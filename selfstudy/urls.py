from django.urls import path
from .views import *


urlpatterns = [
    path('', self_study, name='self_study'),
     path('save-mcq-result/', save_mcq_result, name='save_mcq_result'),
     path('ask-ai/', ask_ai, name='ask_ai'),
]