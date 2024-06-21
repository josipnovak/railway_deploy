from django.contrib import admin
from .models import Option, Person, OneChoiceQuestion, OpinionQuestion, Quiz

# Register your models here.
admin.site.register(Option)
admin.site.register(Person)
admin.site.register(OneChoiceQuestion)
admin.site.register(OpinionQuestion)
admin.site.register(Quiz)