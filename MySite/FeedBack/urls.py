from django.urls import include, path
from .views import feedback_home, feedback_list, add_feedback, average_rating, FeedbackViewSet
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'feedback'

router = DefaultRouter()
router.register(r'api', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', feedback_home, name='feedback_home'),  
    path('<int:job_id>/', feedback_list, name='feedback_list'),
    path('<int:job_id>/add/', add_feedback, name='add_feedback'),
    path('<int:job_id>/average/', average_rating, name='average_rating'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
urlpatterns += router.urls 