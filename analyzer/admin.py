# analyzer/admin.py
from django.contrib import admin
from .models import ReferenceCV, CVAnalysis


@admin.register(ReferenceCV)
class ReferenceCVAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'is_active')
    list_filter = ('is_active', 'uploaded_at')
    search_fields = ('name',)
    ordering = ('-uploaded_at',)


@admin.register(CVAnalysis)
class CVAnalysisAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'reference_cv', 'overall_score', 'analyzed_at')
    list_filter = ('analyzed_at', 'reference_cv')
    search_fields = ('candidate_name', 'reference_cv__name')
    ordering = ('-analyzed_at',)
    readonly_fields = ('analysis_result', 'extracted_text')