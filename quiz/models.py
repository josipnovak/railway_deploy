from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Option(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# abstract class for question
class Question(models.Model):
    text = models.CharField(max_length=100)
    
    def __str__(self):
        return self.text

class OneChoiceQuestion(Question):
    options = models.ManyToManyField(Option, related_name='options')
    
    def __str__(self):
        return self.text
    
class OpinionQuestion(Question):
    answers = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class Quiz(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    quiestions = models.ManyToManyField(OneChoiceQuestion, related_name='questions')
    def __str__(self):
        return self.title
