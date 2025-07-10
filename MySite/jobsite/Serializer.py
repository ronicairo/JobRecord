from rest_framework import serializers
from .models import Category, JobRecord, Contract, Skill, Industry, Candidate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class JobRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRecord
        fields = [
            'id', 'work_year', 'experience_level', 'employment_type',
            'job_title', 'salary', 'salary_currency', 'salary_in_usd',
            'employee_residence', 'remote_ratio', 'company_location', 'company_size'
        ]

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'type_code', 'description']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'location']
