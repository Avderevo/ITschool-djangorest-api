
from django.urls import path
from . import views

urlpatterns = [
    path('',views.ListUsers.as_view()),
    path('<int:pk>/',views.DetailUser.as_view()),
    path('current/',views.CurrentUserView.as_view()),
    path('create-user/',views.UserCreate.as_view())
]
