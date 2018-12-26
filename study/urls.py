
from django.urls import path
from . import views

app_name = 'study'


urlpatterns = [
    path('studyroom/<int:courseid>/', views.LessonVieSet.as_view({'get':'lesson_vs_statistic'})),
    path('course_statistic/<int:userid>/<int:courseid>/', views.LessonVieSet.as_view({'get': 'course_statistic'})),
    path('user_courses/', views.LessonVieSet.as_view({'get': 'user_course_list'})),
    path('course_test/', views.CourseTest.as_view()),
    path('create_message/', views.SaveChatMessage.as_view()),
    path('chat_message/<int:statisticId>/', views.GetChatMessage.as_view({'get':'get_message'})),
    path('one_course/<str:name>/', views.LessonVieSet.as_view({'get': 'one_course'}))

]
