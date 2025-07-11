from django.shortcuts import render, get_object_or_404

from FeedBack import views

def home(request):
    return render(request, 'feedback_home.html')
