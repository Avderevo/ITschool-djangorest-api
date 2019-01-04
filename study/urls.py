
from django.urls import path
from . import views

app_name = 'study'


urlpatterns = [
    path('studyroom/<int:courseId>/', views.LessonVieSet.as_view({'get':'lesson_vs_statistic'}), name='user_statistics'),
    path('course_statistic/<int:courseId>/', views.LessonVieSet.as_view({'get': 'course_statistic'}), name='course_statistic'),
    path('user_courses/', views.LessonVieSet.as_view({'get': 'user_course_list'}), name='user_courses'),
    path('course_test/<int:courseId>/', views.CourseTest.as_view(), name='course_test'),
    path('create_message/', views.SaveChatMessage.as_view()),
    path('chat_message/<int:statisticId>/', views.GetChatMessage.as_view({'get':'get_message'})),
    path('one_course/<int:courseId>/', views.CourseVieSet.as_view({'get': 'one_course'}), name='one_course'),
    path('all_courses/', views.CourseVieSet.as_view({'get': 'all_courses'}), name='all_courses'),
    path('students_statistics/<int:userId>/<int:courseId>/', views.LessonVieSet.as_view({'get': 'get_students_statistics'}), name='student_statistics'),
    path('teacher-courses/', views.LessonVieSet.as_view({'get': 'get_teacher_courses'}), name='teacher-courses'),
    path('change_homework_status/<int:statisticId>/', views.HomeworkStatusChange.as_view(), name='change_homework_status'),

    path('teacher_register/<int:courseId>/', views.RegisterTeacherOnCourse.as_view(), name='register_teacher_course'),

]
