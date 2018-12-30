from django.shortcuts import render
from rest_framework import viewsets
from users.models import Profile
from rest_framework.views import APIView
from .models import Course, Lesson, LessonStatistic, CourseStatistic, Message
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

    def one_course(self, request, name):
        course = Course.objects.get(name_1 = name)
        serializer = serializers.CourseSerializer(course)
        return Response(serializer.data)

    def get_all_students(self, request, id):
        students = User.objects.filter(coursestatistic__course_id = id)
        serializer = serializers.UserSerializer(students, many=True)
        return Response(serializer.data)

    def get_students_statistics(self, request, userId, courseId):
        qs = LessonStatistic.objects.filter(user_id=userId).filter(course_id=courseId)
        serializer = serializers.LessonVsStatisticSerialiser(qs, many=True)
        return Response(serializer.data)


class CourseTest(APIView):

    def post(self, request, name):
        test = request.data['testResult']
        user = request.user
        course = Course.objects.filter(name_1=name).first()
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
    permission_classes = (permissions.AllowAny,)


    def get_message(self, request, statisticId):
        message = Message.objects.filter(lesson_statistic__id = statisticId)
        s = serializers.MessageSerializer(message, many=True)

        return Response(s.data)


'''class CourseTest(APIView):

    def post(self, request, courseid=1):
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
        return Response(status=status.HTTP_400_BAD_REQUEST)'''
