from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile),
    path('course-info/', views.course_info),
    path('forum/', views.get_forum),
    path('assignment/get/', views.get_assignments),
    path('assignment/create/', views.create_assignment),
    path('submit-score/', views.submit_scores),
    path('drop-course/', views.drop_course),
    path('post/create/', views.create_post),
    path('comment/add/', views.add_comment),
    path('csrf-token/', views.csrf_token),
]