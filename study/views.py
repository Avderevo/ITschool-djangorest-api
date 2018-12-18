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
from users.serializers import UserSerializer

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

    def lesson_vs_statistic(self, request, courseid):
        qs = LessonStatistic.objects.filter(user=request.user).filter(course_id=courseid)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)

    def course_statistic(self, request, courseid):
        c = CourseStatistic.objects.filter(user=request.user).filter(course_id=courseid)
        serializer = serializers.CourseStatisticSerializer(c, many=True)

        return  Response(serializer.data)

    def user_course_list(self, request):
        course_stat = CourseStatistic.objects.filter(user = request.user)
        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)




class CourseTest(APIView):

    def post(self, request, courseid=2):
        test = request.data['testResult']
        if test['testResult'] and test['testResult'] == '4':
            user= request.user
            statistic = CourseStatistic.objects.filter(user_id=user.id).filter(course_id=courseid).exists()
            if not statistic:
                course = Course.objects.filter(id = courseid).first()
                course_stat = CourseStatistic()
                course_stat.user = user
                course_stat.course = course
                course_stat.is_active = True
                course_stat.save()
                lessons = Lesson.objects.filter(course_id=courseid)
                for lesson in lessons:
                    lesson_stat = LessonStatistic()
                    lesson_stat.lesson = lesson
                    lesson_stat.user = user
                    lesson_stat.course = course
                    lesson_stat.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)



