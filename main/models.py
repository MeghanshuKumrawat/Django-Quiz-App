from random import choice
from django.db import models
from django.contrib.auth.models import User

lable = (('MCQ', 'MCQ Question'),
        ('LONG', 'Long Question'),
        ('INFO', 'Information'))

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ass_type = models.CharField(choices=lable, max_length=5)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=10, unique=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)  
    marks = models.IntegerField(default=1)
    slug = models.SlugField(max_length=10, unique=True)


    def __str__(self):
        return self.title


class QuizTakers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.user.username

class QuestionAnswer(models.Model):
    qtakers = models.ForeignKey(QuizTakers, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=False)
    slug = models.SlugField()

class LongQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    marks = models.IntegerField(default=1)
    slug = models.SlugField(max_length=10, unique=True)

    