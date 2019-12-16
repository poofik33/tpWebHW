from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404

from .models import Question, Answer, Tag


def index(request):
    questions_page, paginator = paginate(Question.objects.new_questions(), request)
    questions = paginator.get_page(questions_page)
    return render(request, 'questions/index.html', {
        'questions': questions,
        'title': 'New questions',
        'link' : '/hot/',
        'link_title': 'Hot questions'
    })

def ask(request):
    return render(request, 'questions/ask.html')

def login(request):
    return render(request, 'questions/login.html')

def hot(request):
    questions_page, paginator = paginate(Question.objects.hot_questions(), request)
    questions = paginator.get_page(questions_page)
    return render(request, 'questions/index.html', {
        'questions': questions,
        'title': 'Hot questions',
        'link' : '/',
        'link_title': 'New questions'
    })

def settings(request):
    return render(request, 'questions/settings.html')

def signup(request):
    return render(request, 'questions/signup.html')

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