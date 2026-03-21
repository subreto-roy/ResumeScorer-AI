from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    skills = models.JSONField(default=list)
    experience = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    cv_file = models.FileField(upload_to='cvs/')
    created_at = models.DateTimeField(auto_now_add=True)