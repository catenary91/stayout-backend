from django.db import models
from django.utils import timezone

class Member(models.Model):
    student_id = models.IntegerField(primary=True)
    password = models.CharField(max_length=100)
    
    user_key = models.CharField(max_length=100, blank=True)
    register_key = models.CharField(max_length=100)
    
    create_date = models.DateField(default=timezone.now)