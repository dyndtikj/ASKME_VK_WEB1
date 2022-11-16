from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from app.models import *


def paginate(objects_list, request, limit):
    paginator = Paginator(objects_list, limit)
    return paginator.get_page(request.GET.get('page'))


def new_questions(request):
    curr_questions = paginate(Question.objects.all(), request, 5)
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=15)
    return render(request, 'index.html', {'questions': curr_questions,
                                          'paginated_elements': curr_questions,
                                          'popular_tags':  popular_tags,
                                          'best_members': best_members})


def hot_questions(request):
    curr_questions = paginate(Question.objects.hot(), request, 5)
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'hot_questions.html', {'questions': curr_questions,
                                          'paginated_elements': curr_questions,
                                          'popular_tags': popular_tags,
                                          'best_members': best_members})


def questions_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, tag=tag_name)
    curr_questions = paginate(Question.objects.by_tag(tag_name), request, 5)
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'questions_by_tag.html', {'questions': curr_questions,
                                                     'popular_tags': popular_tags,
                                                     'best_members': best_members,
                                                     'tag': tag,
                                                     'paginated_elements': curr_questions
                                                     })


def question(request, question_id):
    curr_question = get_object_or_404(Question, pk=question_id)
    curr_answers = paginate(Answer.objects.by_question(pk=question_id), request, 5)
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'question.html', {'question': curr_question,
                                             'answers': curr_answers,
                                             'popular_tags': popular_tags,
                                             'best_members': best_members,
                                             'paginated_elements': curr_answers
                                             })


def signup(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'register.html', {'popular_tags': popular_tags,
                                           'best_members': best_members
                                           })


def login(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'login.html', {'popular_tags': popular_tags,
                                          'best_members': best_members
                                          })


def settings(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'settings.html', {'popular_tags': popular_tags,
                                             'best_members': best_members
                                             })


def ask(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.sample_profile(count=20)
    return render(request, 'new_question.html', {'popular_tags': popular_tags,
                                                 'best_members': best_members
                                                 })


# import random
#
# from django.core.paginator import Paginator
# from django.http import *
# from django.shortcuts import render
#
#
# c     lass User:
#     def __init__(self, id, nick, login, email, avatar_src):
#         self.id = id
#         self.nick = nick
#         self.login = login
#         self.email = email
#         self.avatar_src = avatar_src
#         return
#
#
# tags = [
#     "Matan",
#     "C++",
#     "WEB",
#     "AaDS"
# ]
#
# questions = [
#     {
#         "title": f"Очень интересный вопрос{i}",
#         "id": i,
#         "author": f'Студент{i}',
#         "avatar_source_img": "avatar",
#         "answers_count": i,
#         "text": f'Мой вопрос пока не несет никакой смысловой нагрузки но его номер - {i} ',
#         "tags": list(random.choices(tags)),
#         "tags_count": len(tags),
#         "like_count": i,
#         "dislike_count": i,
#     } for i in range(100)
# ]
#
# popular_tags = [f"{tags[i%4]}_{i}" for i in range(20)]
# best_members = [f"Student{i}" for i in range(20)]
# user = User(1, 'Student_Rybin', 'Ryb', 'rybin@mail.ru', 'ava.png')
#
#
# def signup(request):
#     return render(request, 'register.html', {'is_auth': False,
#                                            'popular_tags': popular_tags,
#                                            'best_members': best_members
#                                            })
#
#
# def login(request):
#     return render(request, 'login.html', {'is_auth': False,
#                                           'popular_tags': popular_tags,
#                                           'best_members': best_members
#                                           })
#
#
# def settings(request):
#     return render(request, 'settings.html', {'is_auth': True,
#                                              'user': user,
#                                              'popular_tags': popular_tags,
#                                              'best_members': best_members
#                                              })
#
#
# def ask(request):
#     return render(request, 'new_question.html', {'is_auth': True,
#                                                  'user': user,
#                                                  'popular_tags': popular_tags,
#                                                  'best_members': best_members
#                                                  })
#
#
#
#
#
# def questions_by_tag(request, tag_name):
#     tagged_q = []
#     for q in questions:
#         for t in q.get("tags"):
#             if (t == tag_name):
#                 tagged_q.append(q)
#
#     paginator = Paginator(tagged_q, 5)
#     page = request.GET.get('page')
#     curr_questions = paginator.get_page(page)
#     return render(request, 'questions_by_tag.html', {'is_auth': True,
#                                                      'user': user,
#                                                      'questions': curr_questions,
#                                                      'popular_tags': popular_tags,
#                                                      'best_members': best_members,
#                                                      'tag_name': tag_name,
#                                                      'paginated_elements': curr_questions
#                                                      })
#
#
# def hot_questions(request):
#     paginator = Paginator(questions, 5)
#     page = request.GET.get('page')
#     curr_questions = paginator.get_page(page)
#     return render(request, 'hot_questions.html', {'is_auth': True,
#                                                   'user': user,
#                                                   'questions': curr_questions,
#                                                   'popular_tags': popular_tags,
#                                                   'best_members': best_members,
#                                                   'paginated_elements': curr_questions
#                                                   })
#
#
# def new_questions(request):
#     paginator = Paginator(questions, 5)
#     page = request.GET.get('page')
#     curr_questions = paginator.get_page(page)
#
#     return render(request, 'index.html', {'is_auth': True,
#                                           'user': user,
#                                           'questions': curr_questions,
#                                           'popular_tags': popular_tags,
#                                           'best_members': best_members,
#                                           'paginated_elements': curr_questions
#                                           })
#
#
# answers = [
#     {
#         "id": i,
#         "author": f'Студент{i}',
#         "avatar_source_img": "avatar",
#         "text": f'Какой-то очень интересный ответ на вопрос {i}',
#         "like_count": i,
#         "dislike_count": i,
#         "correct": (True and (i % 2 == 0))
#     } for i in range(100)
# ]
#
#
# def question(request, question_id):
#     curr_question = questions[0]
#     paginator = Paginator(answers, 7)
#     page = request.GET.get('page')
#     curr_answers = paginator.get_page(page)
#     return render(request, 'question.html', {'is_auth': True,
#                                              'user': user,
#                                              'question': curr_question,
#                                              'answers': curr_answers,
#                                              'popular_tags': popular_tags,
#                                              'best_members': best_members,
#                                              'paginated_elements': curr_answers
#                                              })
