"""
URL configuration for JobRecord project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from gc import get_stats
from django.contrib import admin
from django.urls import path, include
from jobsite.views import ContractViewSet, JobRecordViewSet, SkillViewSet, IndustryViewSet, CandidateViewSet, stats_view
from JobRecord import views as core_views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'jobrecords', JobRecordViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'skills', SkillViewSet)     
router.register(r'industry', IndustryViewSet)
router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    path('', core_views.home, name='home'), 
    path("admin/", admin.site.urls),
    path('stats/', stats_view, name='stats'),
    path('feedback/', include('FeedBack.urls', namespace='feedback')),
]
urlpatterns += router.urls