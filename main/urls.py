from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (index, logout_user, Create_mcq_assignment, Create_question_assignment,
Create_info_assignment, Update_assignment, Delete_assignment, update_mcq, delete_mcq, join_test,
take_mcq_test, user_result, delete_response, update_question, delete_question, take_question_test,
question_marking, Create_questions, response)

urlpatterns = [
    path('', index, name='index'),
    path('login', LoginView.as_view(template_name='login_page.html'), name='login'),
    path('logout', logout_user, name='logout'),
    path('create-assignment/mcq', Create_mcq_assignment, name='create-mcq-assignment'),
    path('create-assignment/question', Create_question_assignment, name='create-question-assignment'),
    path('create-assignment/information', Create_info_assignment, name='create-info-assignment'),
    path('create-question/<slug>', Create_questions, name='create-question'),
    path('update-assignment/<slug>', Update_assignment, name='update-assignment'),
    path('delete-assignment/<slug>', Delete_assignment, name='delete-assignment'),
    path('update-mcqs/<slug>', update_mcq, name='update-mcqs'),
    path('delete-mcqs/<slug>', delete_mcq, name='delete-mcqs'),
    path('test', join_test, name='join-test'),
    path('mcq-test/<slug>', take_mcq_test, name='take-mcq-test'),
    path('result/<slug>', user_result, name='result-test'),
    path('delete-response/<slug>', delete_response, name='delete-response'),
    path('update-question/<slug>', update_question, name='update-question'),
    path('delete-question/<slug>', delete_question, name='delete-question'),
    path('question-test/<slug>', take_question_test, name='take-question-test'),
    path('question-marking/<slug>', question_marking, name='question-marking'),
    path('response/<slug>', response, name='response'),

]
