
from django.urls import path
from . import views

app_name = 'study'


urlpatterns = [
    path('studyroom/<int:courseid>/', views.LessonVieSet.as_view({'get':'lesson_vs_statistic'})),
    path('course_statistic/<int:userid>/<int:courseid>/', views.LessonVieSet.as_view({'get': 'course_statistic'})),
    path('user_courses/', views.LessonVieSet.as_view({'get': 'user_course_list'})),
    path('course_test/<str:name>/', views.CourseTest.as_view()),
    path('create_message/', views.SaveChatMessage.as_view()),
    path('chat_message/<int:statisticId>/', views.GetChatMessage.as_view({'get':'get_message'})),
    path('one_course/<str:name>/', views.LessonVieSet.as_view({'get': 'one_course'})),
    path('all_students/<int:id>/', views.LessonVieSet.as_view({'get': 'get_all_students'})),
    path('students_statistics/<int:userId>/<int:courseId>/', views.LessonVieSet.as_view({'get': 'get_students_statistics'}))

]
