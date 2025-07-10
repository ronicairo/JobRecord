from rest_framework import serializers
from .models import Category, Feedback

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'job', 'author_name', 'comment', 'rating']
