# Generated by Django 4.2 on 2024-02-29 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_opinionquestion_user_opinionquestion_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='opinion',
        ),
    ]
