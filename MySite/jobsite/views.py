from django.shortcuts import render
from .models import JobRecord, Contract, Skill, Industry, Candidate
from django.db.models import Avg

def stats_view(request):
    total_jobs = JobRecord.objects.count()
    avg_salary = JobRecord.objects.aggregate(Avg('salary_in_usd'))['salary_in_usd__avg']
    countries = JobRecord.objects.values_list('employee_residence', flat=True).distinct().count()

    context = {
        'total_jobs': total_jobs,
        'avg_salary': round(avg_salary, 2) if avg_salary else 0,
        'country_count': countries,
    }
    return render(request, "stats.html", context)

def home(request):
    return render(request, 'home.html')

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from jobsite.serializer import JobRecordSerializer, ContractSerializer, SkillSerializer, IndustrySerializer, CandidateSerializer
from rest_framework import viewsets

class JobRecordViewSet(viewsets.ModelViewSet):
    queryset = JobRecord.objects.all()
    serializer_class = JobRecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
