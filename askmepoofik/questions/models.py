from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class AnswerManager(models.Manager):
    def answers(self, question_pk):
        return self.filter(question=question_pk)

    def answers_with_rating(self, question_pk):
        answers = self.filter(question=question_pk)
        content = []
        for answer in answers:
            likes = answer.answerlikes_set.all()
            rating = sum([1 if x.rating else -1 for x in likes])
            content.append((answer, rating))
        return content

    

class Answer(models.Model):
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default='')
    datetime_published = models.DateTimeField(verbose_name='Дата публикации')
    correct = models.BooleanField(verbose_name='Правильный ответ')
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class LikeManager(models.Manager):
    def get_rating(self):
        pass

class AnswerLikes(models.Model):
    rating = models.BooleanField(verbose_name='Оценка')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    grade_datetime = models.DateTimeField(verbose_name='Дата выставления')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = LikeManager()

    class Meta:
        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответов'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FilePathField(verbose_name='Аватарка')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class QuestionManager(models.Manager):
    def new_questions(self):
        questions = self.all().order_by('datetime_published')
        return questions

    def hot_questions(self):
        questions = self.all()
        return questions

    def tag_questions(self, tag_name):
        tag = Tag.objects.get(name=tag_name)
        questions = tag.question_set.all()
        return questions


class Question(models.Model):
    title = models.CharField(max_length=127, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_published = models.DateTimeField(verbose_name='Дата публикации')
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class QuestionLikes(models.Model):
    rating = models.BooleanField(verbose_name='Оценка')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    grade_datetime = models.DateTimeField(verbose_name='Дата выставления')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = LikeManager()

    class Meta:
        verbose_name = 'Оценка вопроса'
        verbose_name_plural ='Оценки вопросов'

class Tag(models.Model):
    name = models.CharField(max_length=127, verbose_name='Имя', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'