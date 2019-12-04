# Generated by Django 2.2.6 on 2019-11-05 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answerlikes',
            options={'verbose_name': 'Оценка ответа', 'verbose_name_plural': 'Оценки ответов'},
        ),
        migrations.AlterModelOptions(
            name='questionslikes',
            options={'verbose_name': 'Оценка вопроса', 'verbose_name_plural': 'Оценки вопросов'},
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='questions.Question'),
        ),
    ]