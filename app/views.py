from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.views.decorators.http import require_GET, require_POST

from app.forms import *
from app.models import *

best_members = Profile.objects.sample_profile(count=20)

class HttpResponseAjax(JsonResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super().__init__(kwargs)


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super().__init__(
            status='error', code=code, message=message
        )


def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(
                code="no_auth",
                message=u'Login required',
            )

    return view2

def paginate(objects_list, request, limit):
    paginator = Paginator(objects_list, limit)
    return paginator.get_page(request.GET.get('page'))


@require_GET
def new_questions(request):
    curr_questions = paginate(Question.objects.all(), request, 5)
    popular_tags = Tag.objects.popular_tags()
    # best_members = Profile.objects.sample_profile(count=15)
    return render(request, 'index.html', {'questions': curr_questions,
                                          'paginated_elements': curr_questions,
                                          'popular_tags':  popular_tags,
                                          'user': request.user,
                                          'best_members': best_members,
                                          'redirect_after_logout': reverse('index')})


@require_GET
def hot_questions(request):
    curr_questions = paginate(Question.objects.hot(), request, 5)
    popular_tags = Tag.objects.popular_tags()
    # best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'hot_questions.html', {'questions': curr_questions,
                                                  'paginated_elements': curr_questions,
                                                  'popular_tags':  popular_tags,
                                                  'user': request.user,
                                                  'best_members': best_members,
                                                  'redirect_after_logout': reverse('hot_questions')})


@require_GET
def questions_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, tag=tag_name)
    curr_questions = paginate(Question.objects.by_tag(tag_name), request, 5)
    popular_tags = Tag.objects.popular_tags()
    # best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'questions_by_tag.html', {'questions': curr_questions,
                                                     'popular_tags': popular_tags,
                                                     'best_members': best_members,
                                                     'tag': tag,
                                                     'paginated_elements': curr_questions,
                                                     'user': request.user,
                                                     'redirect_after_logout': tag.get_url})


def question(request, question_id):
    answer_count_on_page = 5
    print(request.GET)
    print(request.POST)
    curr_question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        curr_answers = paginate(Answer.objects.by_question(pk=question_id), request, 5)
        popular_tags = Tag.objects.popular_tags()
        best_members = Profile.objects.sample_profile(count=20)
        return render(request, 'question.html', {'question': curr_question,
                                                 'answers': curr_answers,
                                                 'popular_tags': popular_tags,
                                                 'best_members': best_members,
                                                 'paginated_elements': curr_answers,
                                                 'ask_form': AskForm(),
                                                 'redirect_after_logout': curr_question.get_url(),
                                                 })

    if request.method == 'POST' and request.user.is_authenticated:
        answer_form = AnswerForm(data=request.POST)
        curr_answer = Answer.objects.create(
            text=answer_form.data['text'],
            profile_id=Profile.objects.get(user_id=request.user),
            question_id=curr_question
        )
        curr_question.save()
        curr_answer_index = Answer.objects.all().filter(question_id=question_id).filter(rating__gte=0,
                                                                                        date_create__lt=curr_answer.date_create).count()
        return redirect(curr_question.get_url() + '?page=' +
                        str(curr_answer_index // answer_count_on_page + 1)) #+ '#is-right-checkbox-' + str(curr_answer.pk))


def signup(request):
    print(request.GET)
    print(request.POST)
    popular_tags = Tag.objects.popular_tags()
    # best_members = Profile.objects.sample_profile(count=20)
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(request.POST.get('next', '/'))
        else:
            print("non valid form")
    return render(request, 'register.html', {
        'form': form,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'user': request.user,
    })


def login(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    print(request.GET)
    print(request.POST)
    redirect_page = request.GET.get('next')
    if not redirect_page:
        redirect_page = 'index'

    if request.method == 'GET':
        form = LoginForm()
    else: #request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, 'User not found')
            else:
                auth.login(request, user)
                return redirect(redirect_page)
    return render(request, 'login.html', {'form': form,
                                          'best_members': best_members,
                                          'user': request.user,
                                          'redirect_after_logout': redirect_page,
                                          'popular_tags': popular_tags})


@login_required(login_url='login')
@require_GET
def logout(request):
    print(request.GET)
    print(request.POST)
    auth.logout(request)
    return_page = request.GET.get('next')
    if return_page:
        return redirect(return_page)
    return redirect(reverse('index'))


@login_required(login_url='login')
def settings(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        form = SettingsForm(
            initial={'username': request.user.username, 'email': request.user.email, 'password': request.user.password})
    else:
        form = SettingsForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
    return render(request, 'settings.html', {
        'form': form,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'user': request.user,
    })


@login_required(login_url='login')
def ask(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(request.user.profile, data=request.POST)
        if form.is_valid():
            published_question = form.save()
            return redirect(published_question.get_url())
    return render(request, 'new_question.html', {
        'form': form,
        'popular_tags': popular_tags,
        'best_members': best_members,
    })


@login_required_ajax
@require_POST
def answer_correct(request):
    print(request.POST)
    try:
        answer_id = request.POST['id']
        answer = Answer.objects.get(id=answer_id)
        if answer.question_id.profile_id == request.user.profile:
            answer.change_mind_correct()
            answer.save()
            # return HttpResponseAjax(id=answer_id)
            return HttpResponseAjax()
    except Answer.DoesNotExist:
        return HttpResponseAjaxError(code='bad_params', message='this answer is in an invalid state or does not exist')

    return HttpResponseAjaxError(code='bad_params', message='this answer is in an invalid state or does not exist')


@login_required_ajax
@require_POST
def question_vote(request):
    print(request.POST)
    if request.POST['action'] == "like":
        action = True
    else:
        action = False
    try:
        like = LikeQuestion.objects.get(profile_id=request.user.profile,
                                        question_id=Question.objects.get(id=request.POST['id']))

        if like.is_like == action:
            return HttpResponseAjax(new_rating=like.delete())

        like.change_mind()
        like.save()
        return HttpResponseAjax(new_rating=Question.objects.get(id=request.POST['id']).rating)

    except LikeQuestion.DoesNotExist:
        like = LikeQuestion.objects.create(profile_id=request.user.profile,
                                           question_id=Question.objects.get(id=request.POST['id']),
                                           is_like=action)
        like.save()
        return HttpResponseAjax(new_rating=Question.objects.get(id=request.POST['id']).rating)
    except LikeQuestion.MultipleObjectsReturned:
        return HttpResponseAjaxError(code='bad_params', message='Something is wrong with request. You can try again!')

@login_required_ajax
@require_POST
def answer_vote(request):
    print(request.POST)
    if request.POST['action'] == "like":
        action = True
    else:
        action = False
    try:
        like = LikeAnswer.objects.get(profile_id=request.user.profile,
                                      answer_id=Answer.objects.get(id=request.POST['id']))

        if like.is_like == action:
            return HttpResponseAjax(new_rating=like.delete())

        like.change_mind()
        like.save()
        return HttpResponseAjax(new_rating=Answer.objects.get(id=request.POST['id']).rating)

    except LikeAnswer.DoesNotExist:
        like = LikeAnswer.objects.create(profile_id=request.user.profile,
                                         answer_id=Answer.objects.get(id=request.POST['id']),
                                         is_like=action)
        like.save()
        return HttpResponseAjax(new_rating=Answer.objects.get(id=request.POST['id']).rating)
    except LikeAnswer.MultipleObjectsReturned:
        return HttpResponseAjaxError(code='bad_params', message='Something is wrong with request. You can try again!')
