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
        for user in test_users:
            self.stdout.write('Deleting ' + user.username)
            user.delete()

        test_tags = Tag.objects.filter(name__contains='tag')
        for tag in test_tags:
            self.stdout.write('Deleting ' + tag.name)
            tag.delete()

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
                ql = QuestionLikes(author=user, raiting=rt, grade_datetime=aware_datetime, question=question)
                ql.save()

                ans = Answer(author=user,)


        self.stdout.write('Data added to database')
