from django.db import models
from jobsite.models import JobRecord 

class Feedback(models.Model):
    job = models.ForeignKey(JobRecord, on_delete=models.CASCADE, related_name="feedbacks")
    author_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} ({self.rating}/5)"
