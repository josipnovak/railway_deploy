from django.urls import path, re_path
from django.views.static import serve as static_serve

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('create_quiz/one_choice/', views.create_one_choice, name='create_one_choice'),
    path('create_quiz/anonymous/', views.create_anonymous, name='create_anonymous'),
    path('new_quiz/add_one_choice/', views.add_one_choice, name='add_one_choice'),
    path('new_quiz/add_anonymous/', views.add_anonymous, name='add_anonymous'),
    path('user_quizzes/', views.user_quizzes, name='user_quizzes'),
    path('quiz_details/<int:quiz_id>/', views.quiz_details, name='quiz_details'),
    path('start_screen/<int:quiz_id>/', views.start_screen, name='start_screen'),
    path('send_message/', views.send_message, name='send_message'),
    path('change_screen/<str:code_for_enter>/', views.change_screen, name='change_screen'),
    path('ajax/players_list/<int:quiz_id>/', views.ajax_players_list, name='ajax_players_list'),
    path('start_quiz/<int:quiz_code>/<int:question_number>/', views.start_quiz, name='start_quiz'),
    path('start_quiz_answer/<int:quiz_code>/<int:question_number>/', views.start_quiz_answer, name='start_quiz_answer'),
    path('ajax/quiz_question/<str:quiz_code>/<int:question_number>/', views.ajax_quiz_question, name='ajax_quiz_question'),
    path('finished_quizzes/', views.finished_quizzes, name='finished_quizzes'),
    path('quiz_results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
    path('export_results/<int:quiz_id>/', views.export_results, name='export_results'),
    # Urls for quiz players 
    path('join_quiz/<int:quiz_id>/', views.join_quiz, name='join_quiz'),
    path('loading_screen/<int:quiz_id>/', views.loading_screen, name='loading_screen'),
    path('one_choice_question/<int:quiz_id>/', views.one_choice_question, name='one_choice_question'),
    path('anonymous_question/<int:quiz_id>/', views.anonymous_question, name='anonymous_question'),
    path('current_results/<int:quiz_id>/', views.current_results, name='current_results'),
    path('final_results/<int:quiz_id>/<int:number_of_points>/', views.final_results, name='final_results'),

    re_path(r'^firebase-messaging-sw.js$', static_serve, {'document_root': 'quiz/static/quiz', 'path': 'firebase-messaging-sw.js'}),
]