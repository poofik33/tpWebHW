from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render, get_object_or_404

from .models import Question, Answer, Tag
from questions import forms


def index(request):
    questions_page, paginator = paginate(Question.objects.new_questions(), request)
    questions = paginator.get_page(questions_page)
    return render(request, 'questions/index.html', {
        'questions': questions,
        'title': 'New questions',
        'link' : '/hot/',
        'link_title': 'Hot questions'
    })

@login_required(login_url='login')
def ask(request):
    if request.method == "POST":
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request)
            return redirect('question', question_id=question.id)
    else:
        form = forms.QuestionForm()
    return render(request, 'questions/ask.html', {
        'form': form
    })

def login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.log_in()
            if user:
                user_login(request, user)
                return redirect('index')
    else:
        form = forms.LoginForm()
    return render(request, 'questions/login.html', {
        'form': form
    })

@login_required(login_url='login')
def logout(request):
    user_logout(request)
    return redirect(request)

def hot(request):
    questions_page, paginator = paginate(Question.objects.hot_questions(), request)
    questions = paginator.get_page(questions_page)
    return render(request, 'questions/index.html', {
        'questions': questions,
        'title': 'Hot questions',
        'link' : '/',
        'link_title': 'New questions'
    })

@login_required(login_url='login')
def settings(request):
    if request.method == "POST":
        form = forms.SettingsForm(request.POST)
        if form.is_valid():
            form.save(request.user)
    else:
        user = request.user
        form = forms.SettingsForm({
            'login': user.username,
            'email': user.email
        })
    return render(request, 'questions/settings.html', {
        'form': form
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_login(request, user)
            return redirect('index')
        else:
            pass
    else:
        form = forms.RegistrationForm()
    return render(request, 'questions/signup.html', {
        'form': form
    })

def tag(request, tag_name):
    questions_tag = Question.objects.tag_questions(tag_name)
    questions_page, paginator = paginate(questions_tag, request)
    questions = paginator.get_page(questions_page)
    return render(request, 'questions/index.html', {
        'questions': questions,
        'title': tag_name,
        'link': 0
    })

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers_page, paginator = paginate(Answer.objects.answers_with_rating(question_id), request, 30)
    answers = paginator.get_page(answers_page)
    return render(request, 'questions/question.html', {
        'question': question,
        'answers': answers
    })


def paginate(object_list, request, number=20):
    paginator = Paginator(object_list, number)
    objects_page = request.GET.get('page')
    return objects_page, paginator