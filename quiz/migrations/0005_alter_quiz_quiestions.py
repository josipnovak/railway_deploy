# Generated by Django 4.2 on 2024-02-29 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_remove_person_opinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiestions',
            field=models.ManyToManyField(related_name='questions', to='quiz.onechoicequestion'),
        ),
    ]
