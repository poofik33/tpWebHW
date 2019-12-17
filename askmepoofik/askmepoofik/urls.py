"""askmepoofik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from questions import views as questions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', questions.index, name="index"),
    path('ask/', questions.ask, name="ask"),
    path('hot/', questions.hot, name="hot"),
    path('login/', questions.login, name="login"),
    path('logout/', questions.logout, name="logout"),
    path('question/<int:question_id>/', questions.question, name="question"),
    path('settings/', questions.settings, name="profile"),
    path('signup/', questions.signup, name="registration"),
    path('tag/<str:tag_name>/', questions.tag, name="tag"),
]
