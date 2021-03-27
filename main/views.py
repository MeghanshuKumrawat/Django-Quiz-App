from django.db.models.fields import SlugField
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, QuestionUpdateForm
from .models import Assignment, Question, QuizTakers, QuestionAnswer, LongQuestion
from django.utils import timezone
from .templatetags import tags
import random, string

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

def update_profile(request):
    if request.user.is_authenticated:
        update_form = UserUpdateForm(request.POST or None, instance=request.user)
        assignments = Assignment.objects.filter(user=request.user).order_by('-date')
        if update_form.is_valid():
            update_form.save()
    else:
        update_form = UserUpdateForm()
    return update_form

def index(request):
    registration_form = UserCreationForm(request.POST or None)
    if registration_form.is_valid():
        user = registration_form.save()
        login(request, user)
    
    if request.user.is_authenticated:
        update_form = UserUpdateForm(request.POST or None, instance=request.user)
        assignments = Assignment.objects.filter(user=request.user).order_by('-date')
        if update_form.is_valid():
            update_form.save()
    else:
        update_form = UserUpdateForm()
        assignments = None
    context = {'registration_form':registration_form, 
             'update_form':update_form,
             'assignments':assignments}
    return render(request, 'index.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

@login_required
def Create_mcq_assignment(request):
    if request.method == 'POST':
        assignment = Assignment.objects.create(user=request.user,
                                                title=request.POST.get('title'),
                                                description=request.POST.get('description'),
                                                ass_type='MCQ',
                                                slug=rand_slug())
        assignment.save()
        return redirect('create-question', slug=assignment.slug)
    context = {'update_form':update_profile(request)}
    return render(request, 'create_assignment.html', context)

@login_required
def Create_question_assignment(request):
    if request.method == 'POST':
        assignment = Assignment.objects.create(user=request.user,
                                                title=request.POST.get('title'),
                                                description=request.POST.get('description'),
                                                ass_type='LONG',
                                                slug=rand_slug())
        assignment.save()
        return redirect('create-question', slug=assignment.slug)
    context = {'update_form':update_profile(request)}
    return render(request, 'create_assignment.html', context)

@login_required
def Create_info_assignment(request):
    if request.method == 'POST':
        assignment = Assignment.objects.create(user=request.user,
                                                title=request.POST.get('title'),
                                                description=request.POST.get('description'),
                                                ass_type='INFO',
                                                slug=rand_slug())
        assignment.save()
        return redirect('index')
    context = {'update_form':update_profile(request)}
    return render(request, 'create_assignment.html', context)

@login_required
def Update_assignment(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    if request.method == 'POST':
        assignment.title=request.POST.get('title')
        assignment.description=request.POST.get('description')
        assignment.save()
        return redirect('create-question', slug=assignment.slug)
    context = {'assignment':assignment, 'update_form':update_profile(request)}
    return render(request, 'update_assignment.html', context)

@login_required
def Delete_assignment(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    assignment.delete()
    return redirect('index')

@login_required
def Create_questions(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    if assignment.ass_type == 'MCQ':
        questions = Question.objects.filter(assignment=assignment)
        if request.method == 'POST':
            question = Question.objects.create(assignment=assignment,
                                                title=request.POST.get('title'),
                                                option_1=request.POST.get('option_1'),
                                                option_2=request.POST.get('option_2'),
                                                option_3=request.POST.get('option_3'),
                                                option_4=request.POST.get('option_4'),
                                                answer=request.POST.get('answer'),
                                                marks=request.POST.get('marks'),
                                                slug=rand_slug())
        context = {'assignment':assignment, 'questions':questions, 'update_form':update_profile(request)}
        return render(request, 'mcq_create.html', context)

    elif assignment.ass_type == 'LONG':
        questions = LongQuestion.objects.filter(assignment=assignment)
        if request.method == 'POST':
            LongQuestion.objects.create(assignment=assignment,
                                            title=request.POST.get('title'),
                                            marks=request.POST.get('marks'),
                                            slug=rand_slug())
        context = {'assignment':assignment, 'questions':questions, 'update_form':update_profile(request)}
        return render(request, 'question_create.html', context)

    else:
        return redirect('index')

@login_required
def update_mcq(request, slug):
    question = get_object_or_404(Question, slug=slug)
    if request.method == 'POST':
        question.title=request.POST.get('title')
        question.option_1=request.POST.get('option_1')
        question.option_3=request.POST.get('option_3')
        question.option_2=request.POST.get('option_2')
        question.option_4=request.POST.get('option_4')
        question.answer=request.POST.get('answer')
        question.marks=request.POST.get('marks')
        question.save()
        return redirect('create-question', slug=question.assignment.slug)
    context = {'question':question, 'update_form':update_profile(request)}
    return render(request, 'mcq_update.html', context)

@login_required
def update_question(request, slug):
    question = get_object_or_404(LongQuestion, slug=slug)
    if request.method == 'POST':
        question.title=request.POST.get('title')
        question.marks=request.POST.get('marks')
        question.save()
        return redirect('create-question', slug=question.assignment.slug)
    context = {'question':question, 'update_form':update_profile(request)}
    return render(request, 'longquestion_update.html', context)

@login_required
def delete_mcq(request, slug):
    question = get_object_or_404(Question, slug=slug)
    question.delete()
    return redirect('create-question', slug=question.assignment.slug)

@login_required
def delete_question(request, slug):
    question = get_object_or_404(LongQuestion, slug=slug)
    question.delete()
    return redirect('create-question', slug=question.assignment.slug)

@login_required
def join_test(request):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, slug=request.POST.get('slug'))
        qs = QuizTakers.objects.filter(user=request.user, assignment__slug=assignment.slug)
        if qs:
            return redirect('result-test', slug=assignment.slug) 
        else:
            takers = QuizTakers.objects.create(user=request.user, assignment=assignment, slug=rand_slug())
            
            if assignment.ass_type == 'MCQ':
                questions = Question.objects.filter(assignment=takers.assignment)
                for que in questions:
                    QuestionAnswer.objects.create(qtakers=takers, question=que.title, slug=rand_slug())
                return redirect('take-mcq-test', slug=assignment.slug)
            elif assignment.ass_type == 'LONG':
                questions = LongQuestion.objects.filter(assignment=takers.assignment)
                for que in questions:
                    QuestionAnswer.objects.create(qtakers=takers, question=que.title, slug=rand_slug())
                return redirect('take-question-test', slug=assignment.slug)
            elif assignment.ass_type == 'INFO':
                return redirect('index')
            else:
                return redirect('index')
    context = {'update_form':update_profile(request)}
    return render(request, 'join_test.html', context)

@login_required
def take_mcq_test(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    questions = Question.objects.filter(assignment=assignment)
    qtakers = get_object_or_404(QuizTakers, user=request.user, assignment=assignment)
    if request.method == 'POST' and qtakers:
        for question in questions:
            que = get_object_or_404(QuestionAnswer, question=question.title, qtakers=qtakers)
            que.answer = request.POST.get(question.slug)
            que.status = True if question.answer==request.POST.get(question.slug) else False
            que.save()
        qtakers.end_date = timezone.now()
        qtakers.save()
        return redirect('result-test', slug=assignment.slug)
    
    context = {'assignment':assignment, 'questions':questions, 'update_form':update_profile(request)}
    return render(request, 'take_mcq_test.html', context)

@login_required
def take_question_test(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    questions = LongQuestion.objects.filter(assignment=assignment)
    qtakers = get_object_or_404(QuizTakers, user=request.user, assignment=assignment)
    if request.method == 'POST' and qtakers:
        for question in questions:
            que = get_object_or_404(QuestionAnswer, question=question.title, qtakers=qtakers)
            que.answer = request.POST.get(question.slug)
            que.save()
        qtakers.end_date = timezone.now()
        qtakers.save()
        return redirect('result-test', slug=assignment.slug)
    context = {'assignment':assignment, 'questions':questions, 'update_form':update_profile(request)}
    return render(request, 'take_question_test.html', context)

@login_required
def user_result(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    qtakers = get_object_or_404(QuizTakers, user=request.user, assignment=assignment)

    context = {'qtakers':qtakers, 'update_form':update_profile(request)}
    return render(request, 'result.html', context)

@login_required
def response(request, slug):
    assignment = get_object_or_404(Assignment, slug=slug)
    qtakers = QuizTakers.objects.filter(assignment=assignment)
    total_correct_answer = tags.total_correct_answer(assignment.slug)
    questionanswers_list = []
    for que in qtakers:
        questionanswers_list.append(QuestionAnswer.objects.filter(qtakers=que))
    context = {'assignment':assignment, 'zipped_data':zip(qtakers, questionanswers_list, total_correct_answer), 'update_form':update_profile(request)}
    if assignment.ass_type == 'MCQ':
        return render(request, 'mcq_response.html', context)
    elif assignment.ass_type == 'LONG':
        return render(request, 'question_response.html', context)
    else:
        return redirect('index')

@login_required
def delete_response(request, slug):
    qtakers = get_object_or_404(QuizTakers, slug=slug)
    qtakers.delete()
    if qtakers.assignment.ass_type == 'MCQ':
        return redirect('response', slug=qtakers.assignment.slug)
    elif qtakers.assignment.ass_type == 'LONG':
        return redirect('response', slug=qtakers.assignment.slug)
    else:
        return redirect('index')

@login_required
def question_marking(request, slug):
    question = get_object_or_404(QuestionAnswer, slug=slug)
    question.status = False if question.status else True
    question.save()
    return redirect('response', slug=question.qtakers.assignment.slug)