from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    
    
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('tutor/dashboard/', tutor_dashboard, name='tutor_dashboard'),
    
    path('become-tutor/', become_tutor, name='become_tutor'),
    path('become-student/', become_student, name='become_student'),
    
    path('student/profile/', student_profile, name='student_profile'),
]