from asyncio import log
from datetime import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from quiz.models import Quiz
import pyrebase
import random
import firebase_admin
from firebase_admin import credentials, initialize_app, messaging
import os
from supabase import create_client
import qrcode 
import io
import base64

config = {
    "apiKey": "AIzaSyBcSUZ0zXsAEOY9t4PL82NqBKdGJFZgsX0",
    "authDomain": "zavrsni-proba-1.firebaseapp.com",
    "databaseURL": "https://zavrsni-proba-1-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "zavrsni-proba-1",
    "storageBucket": "zavrsni-proba-1.appspot.com",
    "messagingSenderId": "649829209184",
    "appId": "1:649829209184:web:343823581c648622d65f05"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
if not firebase_admin._apps:
    cred = credentials.Certificate({
                "type": "service_account",
                "project_id": "zavrsni-proba-1",
                "private_key_id": "97a26ee5764a24f732c1c8c31f1753c6c01bf6bc",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDWOthavG/nZGgg\nyU5hRlOjfbaaQe1ae3fadkTq4cFaEe0d09OcCi45CnD6V4RpLbXbg0z3ZPIZWONa\nhz1RN6Z8u/Y6xoLBARqEQE+/1WVcEiwJugxdE8CduCZPba5KEh2ZiRS3X865mSQL\n2bPyjxFRLH7+SD9vkBJE6504RWfFK5Ih1W4k2DlOysmYPR6om6IPFApX9RYFhci0\njc2JIkbIGPVhKoHY6TXNqoIJ6PY24TNU71AzTtoLTtRxN82G/xxygd6vi+8RAmYy\nYZm3ydBX2kljbHIup43qgKvbqxrk04Ih2+SjImajl8UMsTCpbFNDXCULgIns/lg/\nZcg9FUu3AgMBAAECggEAA9NchmTzu/ZvZEPUB36sWFtoBbcvAueji0jYuuJkg97q\nv2vx98kNbEKtznqo8wE4TH7lbUw7L+Kwz1liP0S2z2bCjegk8PIRGX2AhGoje5Ju\nK4+hUDmIaLNKKS70kX64p+4/wB/mNCryRC0+E73O+bEeuhxrgurYDgJbILnJ5vEe\nM9zj6GtLBZedMB9r035cg310lQewkdpRjx9KyLLxnJZGX1452b/OISEFIOdG4UEO\nDDCZx7g56tsOm8Og7WTspOtP7fZpcXsK3v12lOaZBOWrgdTmtGUYzODInlxEoi/G\nI4bhBJr/I7+JjjjqgKc1yQmwc+CRiMv5O5q/ZRP4qQKBgQD4CFyg7qvxFAtZit78\ne3wOMMtulTzF0ouRH3pql3khBZupALq/MKZBrukHwN3niW9w0Ltrz7vgClaxSdUe\nO1pX4xyjrQCwuEzyV8KuKnCbCNNDtronTxNEzHXMDaXs6vL+WCTsv/+KBeUeCxR5\nxCV+QqoQaAgcjN3bwox3Ku6buwKBgQDdHIOR8CHCT+ZGnzUqzHi/3iUCwSEa2nwP\nKiTVWPdQ4aX+N+lVJXTtD9lDneYjMildCjjbWbq4lRAGPwfUL1AIn3IrWKc5/sXa\np7oQlem9nzpD1UsAlRrXc0vzUGoqmHK1YFm9A0m1JxClBGzxd3VmoUsqPjBMaVlH\nklzaZ9FKNQKBgGEFxFYfhprTIG1yaS+SjkBuzeT/87neVkH6ckRn5DYKn41If8Ry\nH1bqOLWTuDnuBO24eNf/dpp48NiA7SDaTsi6SmWsMuzt6wuRUNIYP9wlY57FR6RA\nxmTPJfUgEZvPfCYKDMefgzJWg/1wkB3hoFj3ctbgGuwwHkjsnU2wOY4pAoGAT+Y3\n3QqLCG5a5fYt/jM5Bww9D4u+bLe60LgH61hktkNz+jM2C+CnKerqNbbfLKS5sbc5\n6Hm6MW0cB0XLjG80WolTdjpo41ofIO4vHEMv3aemJFD081buBiDRtzC9zHqeKNCS\nXOzNO7rMFvVMcM0cDWQHh1JFnbcL3gMTrpCJXmkCgYEA1eiEi0fKvjS+83Ku6YdV\nTcpyjGK8h8uRQshcXgApfc19kL6BSqo8f23a5FBVhRAfu1dBIIjBiLkJ/JmnhBI4\ngIgKgweHjEpwrYMO/Jo3Dx5unUbC4sLlDNQ/Eh5PYZmsNmHbPdJrrrLxNG7tjCeh\nVxzs964+1Wo26Lz0YfOCIyA=\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-4v8t0@zavrsni-proba-1.iam.gserviceaccount.com",
                "client_id": "111160597895199510004",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4v8t0%40zavrsni-proba-1.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
        }
    )
    initialize_app(cred)

url = "https://kedeahnzxeepqtqkaiqi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlZGVhaG56eGVlcHF0cWthaXFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYzODc5NjQsImV4cCI6MjAzMTk2Mzk2NH0.TmDiS62H4stznxshs62aqnfpvWY1k425pBksY34I6XA"
supabase = create_client(url, key)

# Create your views here.
def index(request):
    context = { }
    if 'token' in request.session:
        try:
            # supabase.auth.get_user(request.session['token'])
            context['user'] = request.session['token']
        except:
            request.session.flush()
        return render(request, 'quiz/index.html', context)
    else:
        return render(request, 'quiz/index.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        try:
            user = supabase.auth.sign_up({ "email": email, "password": password })
            supabase.table('users').insert([{"name": username, 'email': email }]).execute()
            return redirect('quiz:index')
        except:
            messages.info(request, 'Invalid credentials')
            return redirect('quiz:register')    
    return render(request, 'registration/register.html')

def login(request):
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            supabase.auth.sign_in_with_password({ "email": email, "password": password })
            name = supabase.table('users').select("*").eq('email', email).execute()
            request.session['token'] = name.data[0]['name']
            return redirect('quiz:index') 
        except:
            message = "Incorrect email or password"
    return render(request, 'registration/login.html', {'message': message})

def logout(request):
    request.session.flush()
    return redirect('quiz:index')

def create_quiz(request):
    return render(request, 'quiz/create_quiz.html')

def create_one_choice(request):
    return render(request, 'quiz/create_one_choice.html')

def add_one_choice(request):
    if request.method == 'POST':
        one_choice_data(request)
    return redirect('quiz:user_quizzes')

def add_anonymous(request):
    if request.method == 'POST':
        anonymous_data(request)
    return redirect('quiz:user_quizzes')

def create_anonymous(request):
    return render(request, 'quiz/create_anonymous.html')

def one_choice_data(request):
    if 'token' not in request.session:
        return redirect('quiz:login')
    creator = request.session['token']
    quiz_name = request.POST.get('quizName')
    description = request.POST.get('quizDescription')
    # Add quiz to database
    creator_id = supabase.table('users').select('id').eq('name', creator).execute().data[0]['id']
    quiz_id = random.randint(100000, 999999)
    supabase.table('quizzes').insert([{"name": quiz_name, "user_id": creator_id, "description": description, "id": quiz_id, "type": "one_choice"}]).execute()
    quiz_id = supabase.table('quizzes').select('id').eq('name', quiz_name).execute().data[0]['id']
    question = request.POST.getlist('quizQuestion')
    answer1 = request.POST.getlist('quizAnswer1')
    answer2 = request.POST.getlist('quizAnswer2')  
    answer3 = request.POST.getlist('quizAnswer3')
    answer4 = request.POST.getlist('quizAnswer4')
    for i in range(len(question)):
        answer1Correct = request.POST.get('answer1Correct' + str(i)) == 'True'
        answer2Correct = request.POST.get('answer2Correct' + str(i)) == 'True'
        answer3Correct = request.POST.get('answer3Correct' + str(i)) == 'True'
        answer4Correct = request.POST.get('answer4Correct' + str(i)) == 'True' 
        image_url = request.POST.get('image_url' + str(i))
        answers = {
                "answer1": {
                    "text": answer1[i],
                    "correct": answer1Correct
                },
                "answer2": {
                    "text": answer2[i],
                    "correct": answer2Correct
                },
                "answer3": {
                    "text": answer3[i],
                    "correct": answer3Correct
                },
                "answer4": {
                    "text": answer4[i],
                    "correct": answer4Correct
                }
            }
        supabase.table('one_choice_question').insert({
            "quiz_id": quiz_id,
            "text": question[i],
            "answers": json.dumps(answers),
            "image_url": image_url
        }).execute()

def anonymous_data(request):
    if 'token' not in request.session:
        return redirect('quiz:login')
    creator = request.session['token']
    quiz_name = request.POST.get('quizName')
    description = request.POST.get('quizDescription')
    # Add quiz to database
    creator_id = supabase.table('users').select('id').eq('name', creator).execute().data[0]['id']
    quiz_id = random.randint(100000, 999999)
    supabase.table('quizzes').insert([{"name": quiz_name, "user_id": creator_id, "description": description, "id": quiz_id, "type": "anonymous"}]).execute()
    quiz_id = supabase.table('quizzes').select('id').eq('name', quiz_name).execute().data[0]['id']
    question = request.POST.getlist('quizQuestion')
    for i in range(len(question)):
        supabase.table('anonymous_question').insert({
            "quiz_id": quiz_id,
            "text": question[i],
            "answers": json.dumps({})
        }).execute()

def user_quizzes(request):
    creator_id = get_user_id(request.session['token'])
    user_quizzes = supabase.table('quizzes').select("*").eq('user_id', creator_id).execute().data
    one_choice_quizzes = []
    anonymous_quizzes = []
    for quiz in user_quizzes:
        if quiz['type'] == 'one_choice':
            one_choice_quizzes.append(quiz)
        else:
            anonymous_quizzes.append(quiz)
    return render(request, 'quiz/user_quizzes.html', {'one_choice_quizzes': one_choice_quizzes, "anonymous_quizzes": anonymous_quizzes})

def quiz_details(request, quiz_id):
    quiz = get_quiz_data(quiz_id)
    return render(request, 'quiz/quiz_details.html', {'quiz': quiz, 'quiz_id': quiz_id})

def start_screen(request, quiz_id):
    quiz = get_quiz_data(quiz_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"https://proba-deploya.onrender.com/join_quiz/{quiz_id}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    img_data_url = f'data:image/png;base64,{img_data}'

    players = supabase.table('players').select('player_name').eq('quiz_id', quiz_id).execute().data

    questions = quiz['questions']
    ids = []
    for question in questions:
        ids.append(question['id'])
    first_question = min(ids)
    return render(request, 'quiz/start_screen.html', {'quiz': quiz, 'quiz_id': quiz_id, 'code_for_enter': quiz_id, 'img_data_url': img_data_url, 'players': players, 'first_question': first_question})

def ajax_players_list(request, quiz_id):
    quiz = get_quiz_data(quiz_id)
    players = supabase.table('players').select('player_name').eq('quiz_id', quiz_id).execute().data
    return render(request, 'quiz/ajax_players_list.html', {'quiz': quiz, 'quiz_code': quiz_id, 'code_for_enter': quiz_id, 'players': players})

def start_quiz(request, quiz_code, question_number):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get('type') == "one_choice":
            question_number = int(question_number) - 1
            tokens = supabase.table('players').select('fcm_token').eq('quiz_id', quiz_code).execute().data
            tokens = [token['fcm_token'] for token in tokens]
            for device_token in tokens:
                messages = messaging.Message(
                    data={
                        "expired": "true"
                    },
                    token = device_token
                )
                messages = messaging.send(messages)
            return redirect('quiz:start_quiz_answer', quiz_code=quiz_code, question_number=question_number)
    quiz = get_quiz_data(quiz_code)
    questions = quiz['questions']
    ids = []
    for question in questions:
        ids.append(question['id'])
    if int(question_number) not in ids:
        players = supabase.table('players').select('player_name', 'points').eq('quiz_id', quiz_code).execute().data
        players = sorted(players, key=lambda x: x['points'], reverse=True)
        if quiz['type'] == 'one_choice':
            tokens = supabase.table('players').select('fcm_token, points').eq('quiz_id', quiz_code).execute().data
            tokens_and_points = [(item['fcm_token'], item['points']) for item in tokens]
            supabase.table("finished_quizzes").insert([{"quiz_name": quiz['name'], "user_id": get_user_id(request.session['token']), "answers": players, "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}]).execute()
            supabase.table('players').delete().eq('quiz_id', quiz_code).execute()
            print(tokens)
            for device_token, points in tokens_and_points:
                messages = messaging.Message(
                    data={
                        "number_of_points": str(points),
                    },
                    token = device_token
                )
                messages = messaging.send(messages)
            return render(request, 'quiz/quiz_finished.html', {'players': players })
        else:
            supabase.table('players').delete().eq('quiz_id', quiz_code).execute()
            answers = supabase.table('anonymous_question').select('text', 'answers').eq('quiz_id', quiz_code).execute().data
            for answer in answers:
                answer['answers'] = json.loads(answer['answers'])
            supabase.table("anonymous_question").update([{"answers": json.dumps({})}]).eq('quiz_id', quiz_code).execute()
            supabase.table("finished_quizzes").insert([{"quiz_name": quiz['name'], "user_id": get_user_id(request.session['token']), "answers": answers, "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}]).execute()
            return render(request, 'quiz/index.html')
    try:
        question = supabase.table('one_choice_question').select('*').eq('quiz_id', quiz_code).eq('id', question_number).execute().data[0]
    except:
        question = supabase.table('anonymous_question').select('*').eq('quiz_id', quiz_code).eq('id', question_number).execute().data[0]
    question['answers'] = json.loads(question['answers'])
    answers = question['answers']
    answers = json.dumps(answers)
    tokens = supabase.table('players').select('fcm_token').eq('quiz_id', quiz_code).execute().data
    tokens = [token['fcm_token'] for token in tokens]
    if quiz['type'] == 'one_choice':
        for device_token in tokens:
            messages = messaging.Message(
                data={
                    "question": question['text'],
                    "answers": answers,
                    "question_number": str(question_number),
                },
                token = device_token
            )
            messages = messaging.send(messages)
    else:
        for device_token in tokens:
            messages = messaging.Message(
                data={
                    "question": question['text'],
                    "question_number": str(question_number),
                },
                token = device_token
            )
            messages = messaging.send(messages)
    return render(request, 'quiz/start_quiz.html', {'question_number': question_number + 1, 'quiz_code': quiz_code, 'question_type': quiz['type'], 'question': question, 'question_text': question['text'], 'answers': answers})

def start_quiz_answer(request, quiz_code, question_number):
    if request.method == "POST":
        return redirect('quiz:start_quiz', quiz_code=quiz_code, question_number=question_number)
    try:
        question = supabase.table('one_choice_question').select('*').eq('quiz_id', quiz_code).eq('id', question_number).execute().data[0]
    except:
        question = supabase.table('anonymous_question').select('*').eq('quiz_id', quiz_code).eq('id', question_number).execute().data[0]
    question_text = question['text']
    question['answers'] = json.loads(question['answers'])
    correct_answers = []
    for key, value in question['answers'].items():
        try:
            if value['correct'] == True:
                correct_answers.append(value['text'])
        except:
            return redirect('quiz:start_quiz', quiz_code=quiz_code, question_number=question_number+1) 
    question_number += 1
    return render(request, 'quiz/start_quiz_answer.html', {'quiz_code': quiz_code, 'question_number': question_number, 'question_text': question_text, 'correct_answer': correct_answers})

def ajax_quiz_question(request, quiz_code, question_number):
    question = supabase.table('anonymous_question').select('*').eq('quiz_id', quiz_code).eq('id', question_number).execute().data[0] 
    question['answers'] = json.loads(question['answers'])
    question_text = question['text']
    
    return render(request, 'quiz/ajax_quiz_question.html', {'question': question, 'question_text': question_text, 'question_number': question_number, 'quiz_code': quiz_code})

def join_quiz(request, quiz_id):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        device_token = request.POST.get('device_token')
        request.session['device_token'] = device_token
        supabase.table('players').insert([{"player_name": player_name, "quiz_id": quiz_id, "points": 0, "fcm_token": device_token}]).execute()
        return redirect('quiz:current_results', quiz_id=quiz_id)
    return render(request, 'quiz/join_quiz.html', {'quiz_id': quiz_id})

def loading_screen(request, quiz_id):
    if request.method == 'POST':
        if request.POST.get('expired') != "true":
            question = request.POST.get('question')
            question_number = request.POST.get('question_number')
            request.session['question_number'] = question_number
            request.session['question'] = question
            quiz = get_quiz_data(quiz_id)
            if quiz['type'] == 'one_choice':
                answers = request.POST.get('answers')
                request.session['answers'] = answers
                return redirect('quiz:one_choice_question', quiz_id=quiz_id)
            else:
                return redirect('quiz:anonymous_question', quiz_id=quiz_id)
        if request.POST.get('time_run_out') == 'true':
            return redirect('quiz:current_results', quiz_id=quiz_id)
    return render(request, 'quiz/loading_screen.html', {"quiz_id":quiz_id})

def one_choice_question(request, quiz_id):
    question_number = request.session.get('question_number')
    question = request.session.get('question')
    try: 
        answers = json.loads(request.session.get('answers'))
    except:
        answers = {}
    if request.method == 'POST':
        if request.POST.get('time_run_out') == 'true':
            return redirect('quiz:current_results', quiz_id=quiz_id)
        if request.POST.get('answer') == 'True':
            device_token = request.POST.get('device_token')
            points = supabase.table('players').select('points').filter('quiz_id', 'eq', quiz_id).filter('fcm_token', 'eq', device_token).execute().data[0]['points']
            points += 1000
            supabase.table('players').update({"points": points}).filter('quiz_id', 'eq', quiz_id).filter('fcm_token', 'eq', device_token).execute()
        return redirect('quiz:loading_screen', quiz_id=quiz_id)
    return render(request, 'quiz/one_choice_question.html', {'quiz_id': quiz_id, 'question_number': question_number, 'question': question, 'answers': answers})

def anonymous_question(request, quiz_id):
    question_number = request.session.get('question_number')
    question = request.session.get('question')
    if request.method == 'POST':
        if request.POST.get('time_run_out') == 'True':
            return redirect('quiz:current_results', quiz_id=quiz_id)
        if request.POST.get('question') != None:
            question = request.POST.get('question')
            question_number = request.POST.get('question_number')
            request.session['question_number'] = question_number
            request.session['question'] = question
            return redirect('quiz:anonymous_question', quiz_id=quiz_id)
        else:
            device_token = request.POST.get('device_token')
            answer = request.POST.get('answer')
            answers = json.loads(supabase.table('anonymous_question').select('answers').eq('quiz_id', quiz_id).eq('id', question_number).execute().data[0]['answers'])
            answers[device_token] = answer
            supabase.table('anonymous_question').update({"answers": json.dumps(answers)}).eq('quiz_id', quiz_id).eq('id', question_number).execute()
            return redirect('quiz:loading_screen', quiz_id=quiz_id)
    return render(request, 'quiz/anonymous_question.html', {'quiz_id': quiz_id, 'question_number': question_number, 'question': question})

def current_results(request, quiz_id):
    device_token = request.session.get('device_token')
    try:
        points = supabase.table('players').select('points').eq('fcm_token', device_token).eq('quiz_id', quiz_id).execute().data[0]['points']
    except:
        pass
    if request.method == 'POST':
        try:
            number_of_points = int(request.POST.get('number_of_points'))
        except:
            number_of_points = None
        print("BROJ BODOVA: ", request.POST.get('number_of_points'))
        if number_of_points != None:
            return redirect('quiz:final_results', quiz_id=quiz_id, number_of_points=number_of_points)
        question = request.POST.get('question')
        question_number = request.POST.get('question_number')
        request.session['question_number'] = question_number
        request.session['question'] = question
        quiz = get_quiz_data(quiz_id)
        if quiz['type'] == 'one_choice':
            answers = request.POST.get('answers')
            request.session['answers'] = answers
            return redirect('quiz:one_choice_question', quiz_id=quiz_id)
        else:
            return redirect('quiz:anonymous_question', quiz_id=quiz_id)
    return render(request, 'quiz/current_results.html', {'points': points, 'quiz_id': quiz_id})

def get_quiz_data(quiz_id):
    quiz = supabase.table('quizzes').select("*").eq('id', quiz_id).execute().data[0]
    if quiz['type'] == 'one_choice':
        questions = supabase.table('one_choice_question').select('*').eq('quiz_id', quiz_id).execute().data
        for question in questions:
            question['answers'] = json.loads(question['answers'])
    else:   
        questions = supabase.table('anonymous_question').select('*').eq('quiz_id', quiz_id).execute().data
        for question in questions:
            question['answers'] = json.loads(question['answers'])
    quiz['questions'] = questions
    return quiz

def finished_quizzes(request):
    creator_id = get_user_id(request.session['token'])
    finished_quizzes = supabase.table('finished_quizzes').select("*").eq('user_id', creator_id).execute().data
    for quiz in finished_quizzes:
        created_at = datetime.strptime(quiz['created_at'], '%Y-%m-%dT%H:%M:%S%z')
        quiz['created_at'] = created_at.strftime('%d/%m/%Y %H:%M:%S')
    return render(request, 'quiz/finished_quizzes.html', {'quizzes': finished_quizzes})

def get_user_id(name):
    return supabase.table('users').select('id').eq('name', name).execute().data[0]['id']

def quiz_results(request, quiz_id):
    quiz = supabase.table("finished_quizzes").select("*").eq('id', quiz_id).execute().data[0]
    return render(request, 'quiz/quiz_results.html', {'quiz': quiz})

def export_results(request, quiz_id):
    quiz = supabase.table("finished_quizzes").select("*").eq('id', quiz_id).execute().data[0]
    results = ""
    try:
        for question in quiz['answers']:
            results += f"Question: {question['text']}\n"
            for key, value in question['answers'].items():
                results += f"{value}\n"
            results += "\n"
    except:
        for player in quiz['answers']:
            results += f"Player: {player['player_name']} \t"
            results += f"Points: {player['points']}\n"
        results += "\n"
    response = HttpResponse(results, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{quiz["id"]}_results.txt"'
    return response

def final_results(request, quiz_id, number_of_points):
    return render(request, 'quiz/final_results.html', {'points': number_of_points, 'quiz_id': quiz_id})

def change_screen(code_for_enter, question, question_number):
    answers = []
    try:
        for answer in question['answers']:
            answers.append({
                "text": question['answers'][answer]['text'],
                "correct": question['answers'][answer]['correct']
            })
    except:
        pass
    answers_json = json.dumps(answers)
    players = db.child("quizzes").child("active").child(code_for_enter).child("players").get().val()
    tokens = []
    if question['type'] == 'one_correct':
        screen = "Routes.QUESTION_SCREEN"
    else:
        screen = "Routes.ANONYMOUS_QUESTION_SCREEN"
    for player in players.values():
        tokens.append(player['deviceToken'])
    for deviceToken in tokens:
        messages = messaging.Message(
            data={
                "screen": screen,
                "question": question['question'],
                "answers": answers_json,
                "question_number": str(question_number)
            },
            token = deviceToken
        )
        response = messaging.send(messages)
        print('Successfully sent message:', response)

def send_message(request):
    messages = messaging.Message(
        data={
            "screen": "Routes.CODE_ENTER"
        },
        token = 'fVo8gF3DSQyH0MYnNMe5hB:APA91bHeFU7V_0fyhJMkKosiUQYtQewp2AWFJI-2deTGL4fyJoyta8aih16THtGnKpt5dDxtHjMNWZdtSyLHkjZyWx6QJ8lt5B6LWRxPFLyhSXGE57gBrdrf3BIxZdiHeTcQVmwSVlqb'
    )
    response = messaging.send(messages)
    print('Successfully sent message:', response)
    return redirect('quiz:index')