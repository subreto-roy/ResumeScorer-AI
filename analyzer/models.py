from django.db import models


class ReferenceCV(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='reference_cvs/')
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.uploaded_at.strftime('%Y-%m-%d')})"


class CVAnalysis(models.Model):
    reference_cv = models.ForeignKey(ReferenceCV, on_delete=models.CASCADE, related_name='analyses')
    candidate_name = models.CharField(max_length=255, blank=True)
    uploaded_file = models.FileField(upload_to='candidate_cvs/')
    extracted_text = models.TextField(blank=True)

    # Scores
    overall_score = models.FloatField(default=0)
    skills_score = models.FloatField(default=0)
    experience_score = models.FloatField(default=0)
    education_score = models.FloatField(default=0)
    keywords_score = models.FloatField(default=0)

    # Detailed feedback
    analysis_result = models.JSONField(default=dict)

    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-analyzed_at']

    def __str__(self):
        return f"{self.candidate_name or 'Unknown'} - Score: {self.overall_score:.1f}%"