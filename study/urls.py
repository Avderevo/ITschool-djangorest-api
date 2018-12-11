
from django.urls import path
from . import views

urlpatterns = [
    path('lesson_statistic/<int:userid>/<int:courseid>/', views.LessonVieSet.as_view({'get':'lesson_vs_statistic'})),
    path('course_statistic/<int:userid>/<int:courseid>/', views.LessonVieSet.as_view({'get': 'course_statistic'})),

]
