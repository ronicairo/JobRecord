from django.urls import path
from .views import feedback_home, feedback_list, add_feedback, average_rating

app_name = 'feedback'

urlpatterns = [
    path('', feedback_home, name='feedback_home'),  # ✅ ajout
    path('<int:job_id>/', feedback_list, name='feedback_list'),
    path('<int:job_id>/add/', add_feedback, name='add_feedback'),
    path('<int:job_id>/average/', average_rating, name='average_rating'),
]
