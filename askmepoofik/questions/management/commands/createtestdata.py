from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import make_aware
from questions.models import *

import datetime
import random


class Command(BaseCommand):
    help = 'Adding test data to database'

    def handle(self, *args, **options):
        test_users = User.objects.filter(username__contains='test')
        self.stdout.write('Deleting test users...')
        for user in test_users:
            user.delete()

        test_tags = Tag.objects.filter(name__contains='tag')
        for tag in test_tags:
            self.stdout.write('Deleting test tags..')
            tag.delete()

        self.stdout.write('Creating test tags...')
        for num in range(1,6):
            name = str(num) + 'test'
            password = 'ASDfgh12345'
            user = User.objects.create_user(username=name, password=password)
            user.is_superuser = False
            user.is_staff = False
            user.save()
            
            tag_name = str(num) + 'tag'
            tag = Tag(name=tag_name)
            tag.save()

        self.stdout.write('Creating test users and questions...')
        test_users = User.objects.filter(username__contains='test')
        for user in test_users:
            for num in range(1, 11):
                title = 'Question #' + str(num) + ' by the user ' + user.username
                content = 'Content of ' + title
                
                naive_datetime = datetime.datetime.now()
                naive_datetime.tzinfo  # None

                settings.TIME_ZONE  # 'UTC'
                aware_datetime = make_aware(naive_datetime)
                aware_datetime.tzinfo  # <UTC>

                q = Question(author=user, title=title, content=content, datetime_published=aware_datetime)
                q.save()
                if num % 2 == 1:
                    tags = Tag.objects.all()[0:3]
                else:
                    tags = Tag.objects.all()[3:6]
                q.tags.add(tags[0], tags[1], tags[2])

        self.stdout.write('Creating likes and answers...')
        questions = Question.objects.filter(title__contains='Question')
        for question in questions:
            for user in test_users:
                if random.randint(0,1) == 1:
                    rt = True
                else:
                    rt = False
                naive_datetime = datetime.datetime.now()
                naive_datetime.tzinfo  # None

                settings.TIME_ZONE  # 'UTC'
                aware_datetime = make_aware(naive_datetime)
                aware_datetime.tzinfo  # <UTC>
                ql = QuestionLikes(author=user, rating=rt, grade_datetime=aware_datetime, question=question)
                ql.save()

                content = 'Content of answer of user ' + user.username
                ans = Answer(author=user, content=content, question=question,
                             datetime_published=aware_datetime)
                ans.save()
                for u in test_users:
                    if random.randint(0,1) == 1:
                        rt = True
                    else:
                        rt = False
                    al = AnswerLikes(rating=rt, author=user, grade_datetime=aware_datetime,
                                     answer=ans)
                    al.save()
                rate = [
                    rate.rating for rate in ans.answerlikes_set.all()
                ]
                rate = rate.count(True) - rate.count(False)
                ans.rating = rate
                ans.save()

            rate = [
                rate.rating for rate in question.questionlikes_set.all()]
            rate = rate.count(True) - rate.count(False)
            question.rating = rate
            question.save()

        self.stdout.write('Data added to database')
