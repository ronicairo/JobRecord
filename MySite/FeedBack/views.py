from warnings import filters
from django.shortcuts import render, get_object_or_404, redirect
from .models import Feedback, Category
from jobsite.models import JobRecord
from django.db.models import Avg, Count
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

def dashboard_view(request):
    # Annoter chaque job avec le nombre de feedbacks et la note moyenne
    jobs = JobRecord.objects.annotate(
        nb_feedback=Count('feedbacks'),
        avg_rating=Avg('feedbacks__rating')
    )

    # Jobs avec au moins 1 feedback et une moyenne > 0
    top_rated_jobs = jobs.filter(avg_rating__isnull=False).order_by('-avg_rating')

    # Nombre total de feedbacks avec note >= 4
    nb_feedbacks_pos = Feedback.objects.filter(rating__gte=4).count()

    return render(request, 'dashboard.html', {
        'top_rated_jobs': top_rated_jobs,
        'nb_feedbacks_pos': nb_feedbacks_pos,
    })

from FeedBack.serializer import FeedbackSerializer, CategorySerializer
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']
    ordering = ['rating'] 

def get_queryset(self):
    queryset = Feedback.objects.all()
    job_id = self.request.query_params.get('job')
    min_rating = self.request.query_params.get('min_rating')

    if job_id:
        queryset = queryset.filter(job_id=job_id)
    if min_rating:
        queryset = queryset.filter(rating__gte=min_rating)

    return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
