from django.test import TestCase
import json
from django.urls import reverse
from django.contrib.auth.models import User
import unittest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.tests.test import TokenTestCase
from study.models import Course, Lesson



class LessonVieSet_ApiTest(TokenTestCase):
    client = APIClient()

    def setUp(self):
        super(LessonVieSet_ApiTest, self).setUp()

        self.COURSE_1 = Course.objects.create(
            id = 1,
            name_1="Python",
            name_2="Web Developer",
            homework_all=10,
            description='Python web developer'

        )
        self.COURSE_2 = Course.objects.create(
            id = 2,
            name_1="Java",
            name_2="Developer",
            homework_all=10,
            description='Java developer'

        )

        self.LESSON_1_COURSE_1 = Lesson.objects.create(
            lesson_title = 'python lesson 1',
            is_homework = True,
            homework_title = 'python homework 1',
            lesson_number  = 1,
            course = self.COURSE_1

        )
        self.LESSON_2_COURSE_1 = Lesson.objects.create(
            lesson_title='python lesson 2',
            is_homework=True,
            homework_title='python homework 2',
            lesson_number=2,
            course = self.COURSE_1

        )

        self.LESSON_1_COURSE_2 = Lesson.objects.create(
            lesson_title='java lesson 1',
            is_homework=True,
            homework_title='java homework 1',
            lesson_number=1,
            course = self.COURSE_2

        )
        self.LESSON_2_COURSE_2 = Lesson.objects.create(
            lesson_title='java lesson 2',
            is_homework=True,
            homework_title='java homework 2',
            lesson_number=2,
            course=self.COURSE_2
        )

    def course_test_done(self, courseId):
        token = self.get_token('test_user', "testing")
        url = reverse('study:course_test', kwargs={'courseId': courseId})
        self.client.post(url, headers={'token': token}, data={"testResult": {'testResult': '4'}},
                                    format='json')

    def test_course_test_done(self):
        token = self.get_token('test_user', "testing")
        url = reverse('study:course_test', kwargs={'courseId': self.COURSE_1.id})
        response = self.client.post(url,  headers={'token':token}, data={"testResult":{'testResult':'4'}}, format='json')
        self.assertEqual(201, response.status_code)

    def test_repeated_course_test_done(self):
        token = self.get_token('test_user', "testing")
        url = reverse('study:course_test', kwargs={'courseId': self.COURSE_1.id})
        self.client.post(url, headers={'token': token}, data={"testResult": {'testResult': '4'}},
                                    format='json')
        response = self.client.post(url, headers={'token': token}, data={"testResult": {'testResult': '4'}},
                                    format='json')

        self.assertEqual(400, response.status_code)


    def test_lesson_vs_statistic(self):
        self.course_test_done(self.COURSE_1.id)

        token = self.get_token('test_user', "testing")
        url = reverse(
            "study:user_statistics", kwargs={'courseId':self.COURSE_1.id}
        )
        response = self.client.get(url, headers={'token':token})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data[0]['lesson']['id'], 1)
        self.assertEqual(response.data[1]['lesson']['id'], 2)

    def test_course_statistic(self):
        token = self.get_token('test_user', "testing")
        url = reverse(
            "study:course_statistic", kwargs={'courseId': self.COURSE_1.id}
        )
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(200, response.status_code)

    def test_user_course_list(self):
        token = self.get_token('test_user', "testing")
        self.course_test_done(self.COURSE_1.id)
        self.course_test_done(self.COURSE_2.id)
        url = reverse(
            "study:user_courses"
        )
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['course']['name_1'], self.COURSE_1.name_1)
        self.assertEqual(response.data[1]['course']['name_1'], self.COURSE_2.name_1)

    def test_get_students_statistics(self):
        token = self.get_token('test_user', "testing")
        self.course_test_done(self.COURSE_1.id)
        url = reverse('study:student_statistics', kwargs={'userId':self.user.id, 'courseId':self.COURSE_1.id})
        response = self.client.get(url, headers={'token': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['course']['id'], self.COURSE_1.id)
        self.assertEqual(response.data[0]['lesson']['lesson_title'], self.LESSON_1_COURSE_1.lesson_title)










