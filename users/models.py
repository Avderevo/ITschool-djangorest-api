from django.db import models
from django.contrib.auth.models import User
from study.models import Course, Lesson


class Activation(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Профиль {self.user}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = 'Профиль пользователей'

