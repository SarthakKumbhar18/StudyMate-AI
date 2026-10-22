from django.urls import path

from .views import *


urlpatterns = [
    path('',my_courses,name='my_courses'),
    path('create/',create_course,name='create_course'),
    path('<int:course_id>/manage/',manage_course,name='manage_course'),
    path('<int:course_id>/add-section/',add_section,name='add_section'),
    path('<int:course_id>/learn/',course_learning,name='course_learning'),

    path('<int:course_id>/',course_detail,name='course_detail'),
    path('section/<int:section_id>/edit/',edit_section,name='edit_section'),
    path('section/<int:section_id>/delete/',delete_section,name='delete_section'),
    path('section/<int:section_id>/quiz/',manage_quiz,name='manage_quiz'),
    path('quiz/<int:quiz_id>/add-question/',add_question,name='add_question'),
    path('question/<int:question_id>/edit/',edit_question,name='edit_question'),
    path('question/<int:question_id>/delete/',delete_question,name='delete_question'),
    path('browse/',browse_courses,name='browse_courses'),


    path('<int:course_id>/create-order/',create_course_order,name='create_course_order'),
    path('verify-payment/',verify_course_payment,name='verify_course_payment'),

]