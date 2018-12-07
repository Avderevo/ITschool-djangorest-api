from django.db import models
from django.contrib.auth.models import User
from study.models import Course


class Activation(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(
        Course,
        through='Statistic',
        through_fields=('course', 'user'),

    )


class Statistic(models.Model):
    course = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(Course, on_delete=models.CASCADE)
    homework_done = models.IntegerField(default=0)
    homework_all = models.IntegerField(blank=True)

