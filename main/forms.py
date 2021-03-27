from django import forms
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.forms import fields
from .models import Assignment, Question

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class QuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']