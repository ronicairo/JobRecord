from django.db import models

# Create your models here.
class Contract(models.Model):
    type_code = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type_code

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class JobRecord(models.Model):
    work_year = models.IntegerField()
    experience_level = models.CharField(max_length=5)
    employment_type = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)
    job_title = models.CharField(max_length=200)
    salary = models.FloatField()
    salary_currency = models.CharField(max_length=10)
    salary_in_usd = models.FloatField()
    employee_residence = models.CharField(max_length=100)
    remote_ratio = models.IntegerField()
    company_location = models.CharField(max_length=100)
    company_size = models.CharField(max_length=2)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job_title', 'work_year', 'employee_residence'],
                name='unique_job_per_year_and_location'
            )
    ]
    def __str__(self):
        return f"{self.job_title} ({self.work_year})"

