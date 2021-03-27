from django import template
from django.shortcuts import get_object_or_404
from main.models import Assignment, Question, QuizTakers, QuestionAnswer, LongQuestion

register = template.Library()

@register.filter
def total_marks(slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    if assignment.ass_type == 'MCQ':
        que = Question.objects.filter(assignment=assignment)
    elif assignment.ass_type == 'LONG':
        que = LongQuestion.objects.filter(assignment=assignment)
    else:
        que = None
    marks = 0
    for i in que:
        marks += i.marks
    return marks

@register.filter
def obtained_marks(slug):
    qtakers = get_object_or_404(QuizTakers, slug=slug)
    question = QuestionAnswer.objects.filter(qtakers=qtakers)
    if qtakers.assignment.ass_type == 'MCQ':
        questions = Question.objects.filter(assignment=qtakers.assignment)
    elif qtakers.assignment.ass_type == 'LONG':
        questions = LongQuestion.objects.filter(assignment=qtakers.assignment)
    else:
        questions = None
    marks = 0
    for que, que2 in zip(question, questions):
        if que.status==True: marks += que2.marks
    return marks

@register.filter
def total_responses(slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    qtakers = QuizTakers.objects.filter(assignment=assignment).count()
    return qtakers

@register.filter
def total_correct_answer(slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    qtakers = QuizTakers.objects.filter(assignment=assignment)
    questionanswers = []
    for que in qtakers:
        questionanswer = QuestionAnswer.objects.filter(qtakers=que, status=True).count()
        questionanswers.append(questionanswer)
    return questionanswers