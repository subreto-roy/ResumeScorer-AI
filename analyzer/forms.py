from django import forms
from .models import ReferenceCV, CVAnalysis


class ReferenceCVForm(forms.ModelForm):
    class Meta:
        model = ReferenceCV
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Senior Python Developer Reference'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.doc,.txt'
            }),
        }


class CandidateCVForm(forms.Form):
    reference_cv = forms.ModelChoiceField(
        queryset=ReferenceCV.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Reference CV"
    )
    candidate_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx,.doc,.txt'
        }),
        label="Upload Candidate CV"
    )