from django.contrib.auth import authenticate
from django import forms
from questions import models

import datetime

class LoginForm(forms.Form):
    login = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'Login'
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'Password'
        }
    ))

    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']

        user = authenticate(username=login, password=password)
        if not user:
            raise forms.ValidationError('Login or password is incorrect')
        return self.cleaned_data

    def log_in(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']
        user = authenticate(username=login, password=password)
        return user



class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'id': 'Email'
            }
    ))
    login = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'Nickname'
            }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'Password'
            }
    ))
    password_repeat = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'Rep-Password'
            }
    ))
    avatar = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'custom-file-input',
            'id': 'avatar-file'
            }
    ))

    def clean(self):
        cpassword = self.cleaned_data['password']
        cpassword_repeat = self.cleaned_data['password_repeat']
        if cpassword != cpassword_repeat:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    def clean_email(self):
        cemail = self.cleaned_data['email']
        print(cemail)
        users = models.User.objects.filter(email=cemail)
        if users:
            raise forms.ValidationError('This email address already exists')
        return cemail

    def clean_login(self):
        clogin = self.cleaned_data['login']
        users = models.User.objects.filter(username=clogin)
        if users:
            raise forms.ValidationError('This username already exists')
        return clogin

    def save(self):
        data = self.cleaned_data
        user = models.User.objects.create_user(
            email=data['email'],
            username=data['login'],
            password=data['password']
            )
        models.Profile.objects.create(user=user)
        return user


class SettingsForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'id': 'Email'
            }
    ))
    login = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'Nickname'
            }
    ))
    avatar = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            'class': 'custom-file-input',
            'id': 'avatar-file'
            }
    ))

    def save(self, req_user):
        user = models.User.objects.get(id=req_user.id)
        data = self.cleaned_data
        u = models.User.objects.get(email=data['email'])
        if not u is user:
            raise forms.ValidationError('User with this email already exist')
        u = models.User.objects.get(username=data['login'])
        if not u is user:
            raise forms.ValidationError('User with this login already exist')
        user = models.User.objects.update(
            email=data['email'],
            username=data['login']
        )

class QuestionForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'Title',
            'placeholder': 'Enter title'
            }
    ))
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'Text',
            'placeholder': 'Input question text'
            }
    ))
    tags = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'Tags',
            'placeholder': 'Enter tags'
            }
    ))

    def clean_tags(self):
        str_tags = self.cleaned_data['tags'].split(', ')
        tags = []
        for t in str_tags:
            tag = models.Tag.objects.filter(name=t)
            if tag:
                tags.append(tag[0])
            else:
                tags.append(models.Tag.objects.create(name=t))
        return tags

    def save(self, request):
        data = self.cleaned_data
        tags = data['tags']
        question = models.Question.objects.create(
            title=data['title'],
            content=data['content'],
            author=request.user,
            datetime_published=datetime.datetime.now()
        )
        question.tags.add(tags[0], tags[1], tags[2])
        return question
