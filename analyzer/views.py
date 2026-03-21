from django.shortcuts import render
from .models import Candidate

def dashboard(request):
    candidates = Candidate.objects.all().order_by('-score')
    return render(request, "dashboard.html", {"candidates": candidates})