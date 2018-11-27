from django.db import models
from django.contrib.auth.models import User



class Course(models.Model):
    title_1 = models.CharField(max_length=50)
    title_2 = models.CharField(max_length=150)
    start_date_description = models.CharField(max_length=150)
    description = models.TextField()




class Activation(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
