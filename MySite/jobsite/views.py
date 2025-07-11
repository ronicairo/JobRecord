from django.shortcuts import render, get_object_or_404
from .models import JobRecord, Contract, Skill, Industry, Candidate
from django.db.models import Avg, Count
from rest_framework.response import Response

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

def job_detail(request, id):
    job = get_object_or_404(JobRecord, id=id)
    return render(request, 'views_details_job.html', {'job': job})

def home(request):
    return render(request, 'home.html')

from rest_framework.permissions import IsAuthenticated
from jobsite.serializer import JobRecordSerializer, ContractSerializer, SkillSerializer, IndustrySerializer, DashboardSerializer, CandidateSerializer
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

class JobRecordPagination(PageNumberPagination):
    page_size = 10

class JobRecordViewSet(viewsets.ModelViewSet):
    queryset = JobRecord.objects.all()
    serializer_class = JobRecordSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job_title']
    ordering_fields = ['salary'] 
    pagination_class = JobRecordPagination

    
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['contract_type']

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = JobRecord.objects.annotate(
            avg_rating=Avg('feedback__rating'),
            feedback_count=Count('feedback')
        ).values('job_title', 'avg_rating', 'feedback_count')
        return Response(queryset)
    
def dashboard_api(request):
    jobs = JobRecord.objects.annotate(
        avg_rating=Avg('feedback__rating'),
        feedback_count=Count('feedback')
    )
    serializer = DashboardSerializer(jobs, many=True)
    return Response(serializer.data)