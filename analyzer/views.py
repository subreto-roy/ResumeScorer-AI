import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import ReferenceCV, CVAnalysis
from .forms import ReferenceCVForm, CandidateCVForm
from .services import extract_text_from_file, analyze_cv_with_grok


def home(request):
    """Dashboard with stats."""
    total_references = ReferenceCV.objects.filter(is_active=True).count()
    total_analyses = CVAnalysis.objects.count()
    recent_analyses = CVAnalysis.objects.select_related('reference_cv').order_by('-analyzed_at')[:5]

    context = {
        'total_references': total_references,
        'total_analyses': total_analyses,
        'recent_analyses': recent_analyses,
    }
    return render(request, 'analyzer/home.html', context)


def upload_reference(request):
    """Upload a reference CV."""
    if request.method == 'POST':
        form = ReferenceCVForm(request.POST, request.FILES)
        if form.is_valid():
            ref_cv = form.save(commit=False)
            ref_cv.save()

            # Extract text
            file_path = os.path.join(settings.MEDIA_ROOT, ref_cv.file.name)
            try:
                ref_cv.extracted_text = extract_text_from_file(file_path)
                ref_cv.save()
                messages.success(request, f'Reference CV "{ref_cv.name}" uploaded successfully!')
            except Exception as e:
                messages.warning(request, f'CV saved but text extraction failed: {str(e)}')

            return redirect('analyzer:reference_list')
    else:
        form = ReferenceCVForm()

    return render(request, 'analyzer/upload_reference.html', {'form': form})


def reference_list(request):
    """List all reference CVs."""
    references = ReferenceCV.objects.all()
    return render(request, 'analyzer/reference_list.html', {'references': references})


def delete_reference(request, pk):
    """Delete a reference CV."""
    ref = get_object_or_404(ReferenceCV, pk=pk)
    if request.method == 'POST':
        ref.delete()
        messages.success(request, 'Reference CV deleted.')
        return redirect('analyzer:reference_list')
    return render(request, 'analyzer/confirm_delete.html', {'object': ref})


def analyze_cv(request):
    """Upload candidate CV and analyze against reference."""
    if request.method == 'POST':
        form = CandidateCVForm(request.POST, request.FILES)
        if form.is_valid():
            reference_cv = form.cleaned_data['reference_cv']
            candidate_file = request.FILES['candidate_file']

            # Save candidate file temporarily
            import tempfile
            suffix = os.path.splitext(candidate_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                for chunk in candidate_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            try:
                # Extract text
                candidate_text = extract_text_from_file(tmp_path)

                if not candidate_text:
                    messages.error(request, 'Could not extract text from the uploaded CV.')
                    return redirect('analyzer:analyze')

                if not reference_cv.extracted_text:
                    messages.error(request, 'Reference CV has no extracted text. Please re-upload it.')
                    return redirect('analyzer:analyze')

                # Analyze with Grok
                result = analyze_cv_with_grok(reference_cv.extracted_text, candidate_text)

                # Save analysis
                # Re-save file to media
                candidate_file.seek(0)
                analysis = CVAnalysis(
                    reference_cv=reference_cv,
                    candidate_name=result.get('candidate_name', 'Unknown'),
                    extracted_text=candidate_text,
                    overall_score=result.get('overall_score', 0),
                    skills_score=result.get('skills_score', 0),
                    experience_score=result.get('experience_score', 0),
                    education_score=result.get('education_score', 0),
                    keywords_score=result.get('keywords_score', 0),
                    analysis_result=result,
                )
                analysis.uploaded_file.save(candidate_file.name, candidate_file, save=True)

                return redirect('analyzer:result', pk=analysis.pk)

            except Exception as e:
                messages.error(request, f'Analysis failed: {str(e)}')
                return redirect('analyzer:analyze')
            finally:
                os.unlink(tmp_path)
    else:
        form = CandidateCVForm()

    return render(request, 'analyzer/analyze.html', {'form': form})


def result(request, pk):
    """Show analysis result."""
    analysis = get_object_or_404(CVAnalysis, pk=pk)
    scores = [
        ('Skills Match', analysis.skills_score),
        ('Experience Match', analysis.experience_score),
        ('Education Match', analysis.education_score),
        ('Keywords Match', analysis.keywords_score),
    ]
    return render(request, 'analyzer/result.html', {'analysis': analysis, 'scores': scores})


def history(request):
    """Show all past analyses."""
    analyses = CVAnalysis.objects.select_related('reference_cv').all()
    return render(request, 'analyzer/history.html', {'analyses': analyses})