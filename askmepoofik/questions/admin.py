from django.contrib import admin
from .models import Question, Profile, Answer, QuestionLikes, AnswerLikes, Tag

# Register your models here.
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Answer)
admin.site.register(AnswerLikes)
admin.site.register(QuestionLikes)
admin.site.register(Tag)