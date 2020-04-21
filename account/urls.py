from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile),
    path('course-info/', views.course_info),
    path('forum/', views.get_forum),
]