from django.shortcuts import render
from .models import JobRecord
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
