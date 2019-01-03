from django.shortcuts import render
from rest_framework import viewsets
from users.models import Profile
from rest_framework.views import APIView
from .models import Course, Lesson, LessonStatistic, CourseStatistic, Message
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from . import serializers
from users.serializers import UserSerializer



class LessonVieSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def lesson_vs_statistic(self, request, courseId):
        qs = LessonStatistic.objects.filter(user=request.user).filter(course_id=courseId)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)

    def course_statistic(self, request, courseId):
        c = CourseStatistic.objects.filter(user=request.user).filter(course_id=courseId).first()
        serializer = serializers.CourseStatisticSerializer(c)
        return  Response(serializer.data)

    def user_course_list(self, request):
        course_stat = CourseStatistic.objects.filter(user = request.user)
        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)

    def get_students_statistics(self, request, userId, courseId):
        qs = LessonStatistic.objects.filter(user_id=userId).filter(course_id=courseId)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)

    def get_teacher_courses(self, request):
        user = request.user
        if user.profile.is_teacher:
            course_stat = CourseStatistic.objects.filter(user=request.user)
        else:
            course_stat=[]
        serializer = serializers.CourseStatisticSerializer(course_stat, many=True)
        return Response(serializer.data)



class CourseVieSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def one_course(self, request, courseId):
        course = Course.objects.filter(id=courseId).first()
        serializer = serializers.CourseSerializer(course)
        return Response(serializer.data)



class HomeworkStatusChange(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, statisticId):
        statistic = LessonStatistic.objects.filter(id = statisticId).first()
        stat = request.data['status']
        statistic.homework_status = int(stat)
        statistic.save()
        return Response(status=status.HTTP_201_CREATED)


class CourseTest(APIView):

    def post(self, request, courseId):
        test = request.data['testResult']
        user = request.user
        course = Course.objects.filter(id=courseId).first()
        statistic = CourseStatistic.objects.filter(user_id=user.id).filter(course_id=course.id).exists()
        if not statistic:
            if test['testResult'] and test['testResult'] == '4':
                course_stat = CourseStatistic()
                course_stat.user = user
                course_stat.course = course
                course_stat.is_active = True
                course_stat.save()
                lessons = Lesson.objects.filter(course_id=course.id)
                for lesson in lessons:
                    lesson_stat = LessonStatistic()
                    lesson_stat.lesson = lesson
                    lesson_stat.user = user
                    lesson_stat.course = course
                    lesson_stat.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SaveChatMessage(APIView):
    def post(self, request ):
        data = request.data
        user = request.user
        statistic = LessonStatistic.objects.filter(id = data['statisticId']).first()
        message = Message()
        message.lesson_statistic = statistic
        message.message_body = data['message']
        message.user = user
        message.save()
        return Response(status=status.HTTP_201_CREATED)


class GetChatMessage(viewsets.ViewSet):

    def get_message(self, request, statisticId):
        message = Message.objects.filter(lesson_statistic__id = statisticId)
        s = serializers.MessageSerializer(message, many=True)

        return Response(s.data)


