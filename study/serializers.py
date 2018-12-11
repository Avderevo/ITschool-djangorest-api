from .models import Course, Lesson, Message, LessonStatistic, CourseStatistic
from users.models import  Profile
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from users.serializers import UserSerializer



class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name_1', 'name_2','is_active', 'homework_all'
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('lesson_title', 'is_homework', 'homework_title', 'lesson_number')



class LessonVsStatisticSerialiser(serializers.ModelSerializer):
    lesson = LessonSerializer()
    course = CourseSerializer()
    user = UserSerializer()

    class Meta:
        model = LessonStatistic
        fields = (
            'lesson', 'course', 'homework_status', 'user'
        )


class CourseStatisticSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CourseStatistic
        fields = ('course', 'homework_done')
