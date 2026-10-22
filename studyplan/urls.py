from django.urls import path
from .views import *


urlpatterns = [
    path('', course_list, name='study_plan'),
    path('course/<int:course_id>/',topic_list,name='course_topics'),
    path('topic/<int:topic_id>/',question_list,name='topic_questions'),
    path('question/<int:question_id>/',question_detail,name='question_detail'),
    path('question/<int:question_id>/run/',run_code,name='run_code'),
    path('question/<int:question_id>/submit/',submit_code,name='submit_code'),

]