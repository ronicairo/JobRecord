from django.shortcuts import render, get_object_or_404

from JobRecord import views

def home(request):
    return render(request, 'home.html')
