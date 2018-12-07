from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=128)


class Lesson(models.Model):
    lesson_title = models.CharField(max_length=125)
    is_homework = models.BooleanField(default=False)
    homework_title = models.CharField(max_length=125, blank=True )
    lesson_number = models.IntegerField()

    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Message(models.Model):
    message_body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


