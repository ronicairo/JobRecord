from django.shortcuts import render, get_object_or_404, redirect
from .models import Feedback
from jobsite.models import JobRecord
from django.db.models import Avg
from django.utils import timezone

def feedback_list(request, job_id):
    min_rating = int(request.GET.get('min', 1))
    job = get_object_or_404(JobRecord, id=job_id)
    feedbacks = Feedback.objects.filter(job=job, rating__gte=min_rating)
    return render(request, 'feedback_list.html', {'job': job, 'feedbacks': feedbacks, 'min_rating': min_rating})

def add_feedback(request, job_id):
    job = get_object_or_404(JobRecord, id=job_id)
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        comment = request.POST.get('comment')
        rating = int(request.POST.get('rating'))
        if 1 <= rating <= 5:
            Feedback.objects.create(job=job, author_name=author_name, comment=comment, rating=rating, created_at=timezone.now())
            return redirect('feedback:feedback_list', job_id=job.id)
    return render(request, 'add_feedback.html', {'job': job})

def average_rating(request, job_id):
    job = get_object_or_404(JobRecord, id=job_id)
    average = Feedback.objects.filter(job=job).aggregate(Avg('rating'))['rating__avg']
    return render(request, 'average_rating.html', {'job': job, 'average': average})

def feedback_home(request):
    jobs = JobRecord.objects.all()
    return render(request, 'feedback_home.html', {'jobs': jobs})
