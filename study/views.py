from django.shortcuts import render
from rest_framework import viewsets
from users.models import Profile
from rest_framework.views import APIView
from .models import Course, Lesson, LessonStatistic, CourseStatistic
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status

from users import serializers as user_serializers
from . import serializers

'''
class ProfileViewSet(viewsets.ModelViewSet):
    qs = Profile.objects.all()
    serializer_class = user_serializers.ProfileSerializer


class CourseVieSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def all_course(self):
        queryset = Course.objects.all()

        serializer = serializers.CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def user_course(self, request, id):
        profile = Profile.objects.filter(user_id=id).first()
        queryset = Course.objects.filter(profile = profile)
        serializer = serializers.CourseSerializer(queryset, many=True)
        return  Response(serializer.data)
'''

class LessonVieSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)


    def lesson_vs_statistic(self, request, userid, courseid):
        qs=LessonStatistic.objects.filter(user_id=userid).filter(course_id = courseid)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)

    def course_statistic(self, request, userid, courseid):
        c = CourseStatistic.objects.filter(user_id=userid).filter(course_id=courseid)
        serializer = serializers.CourseStatisticSerializer(c, many=True)

        return  Response(serializer.data)



