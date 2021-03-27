from django.contrib import admin
from .models import Question, Assignment, QuizTakers, QuestionAnswer, LongQuestion

@admin.register(QuizTakers)
class AdminTakers(admin.ModelAdmin):
    list_display = ['user', 'assignment']
    list_filter = ['user', 'assignment']

@admin.register(QuestionAnswer)
class AdminQA(admin.ModelAdmin):
    list_display = ['question', 'answer', 'qtakers', 'status']
    list_filter = ['question', 'answer', 'status']

@admin.register(Question)
class AdminQuestions(admin.ModelAdmin):
    list_display = ['title', 'assignment', 'answer']
    list_filter = ['assignment']

@admin.register(Assignment)
class AdminAssignment(admin.ModelAdmin):
    list_display = ['user', 'title', 'date']
    list_filter = ['user', 'title', 'date']

@admin.register(LongQuestion)
class AdminQuestions(admin.ModelAdmin):
    list_display = ['title', 'assignment', 'marks']
    # list_filter = ['assignment']