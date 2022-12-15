import time

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from app.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from random import choice, sample, randint
from faker import Faker

faker = Faker()
bulkBig = 10000

def add_arguments(self, parser):
    parser.add_argumentparser.add_argument('--ratio', nargs='?', type=int)

def find_el(arr, el):
    ret = []
    for i in range(0, len(arr)):
        if el == arr[i]:
            ret.append(i)
    return ret


def find_dupl(arr1, arr2):
    for i in range(len(arr1)):
        if arr1[i] in arr2:
            return True
    return False

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--ratio', nargs='?', type=int)

    def handle(self, *args, **options):
        ratio = 100
        if options['ratio']:
            ratio = options['ratio']

        ratios = {
            'users': ratio,
            'questions': ratio * 10,
            'answers': ratio * 100,
            'tags': ratio,
            'answersVotes': ratio * 100,
            'questionsVotes': ratio * 100
        }
        self.fill_db(ratios)

    @staticmethod
    def fill_profiles(profile_count, avatar_count=5):
        temp_data_user = []
        temp_data_profile = []

        for i in range(profile_count):
            temp_data_user.append(User(
                is_superuser=False,
                username=faker.unique.user_name(),
                email=faker.email(),
                password='Def_pwd12345'
            ))

            print(f"Profile: {temp_data_user[-1]}, i={i}")

        User.objects.bulk_create(temp_data_user, batch_size=profile_count)

        u = User.objects.all()

        for j in range(0, len(temp_data_user)):
            temp_data_profile.append(Profile(
                user_id=u[j],
                avatar="img/ava" + str(j % avatar_count) + ".png",
            ))

        Profile.objects.bulk_create(temp_data_profile, batch_size=profile_count)


    @staticmethod
    def fill_tags(tag_count):
        tags = []
        for i in range(tag_count):
            try:
                tag = faker.unique.word() + '_' + str(i)
                print(tag)
                tags.append(Tag(tag=tag))
            except Exception:
                pass
        Tag.objects.bulk_create(tags, i+1)

    @staticmethod
    def fill_questions(question_count):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        tag_ids = list(Tag.objects.values_list('tag', flat=True))

        questions = []
        for i in range(question_count):
            questions.append(Question(
                profile_id=Profile.objects.get(pk=choice(profile_ids)),
                title=faker.sentence()[:-1] + '?',
                text=faker.text()
            ))
            print(questions[-1], i)
        Question.objects.bulk_create(questions, i+1)
        q = Question.objects.all()
        for j in range(0, len(q)):
            tags_list = sample(tag_ids, k=randint(1, 3))
            print(tags_list)
            print(Tag.objects.create_question(tags_list))
            #q[j].objects.update(tags_list=Tag.objects.create_question(tags_list))
            q[j].tags.set(Tag.objects.create_question(tags_list))
            q[j].save()
            print(q[j], q[j].tags)


    @staticmethod
    def fill_answers(answer_count):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        ans = []
        for i in range(answer_count):
            ans.append(Answer(
                profile_id=Profile.objects.get(pk=choice(profile_ids)),
                question_id=Question.objects.get(pk=choice(question_ids)),
                text=faker.text(),
                is_correct=faker.random_int(min=0, max=1),
            ))
            print(ans[-1], i)
            if (i + 1) % bulkBig == 0:
                Answer.objects.bulk_create(ans[:bulkBig], bulkBig)
                ans = []
        if len(ans) > 0:
            Answer.objects.bulk_create(ans[:len(ans)], len(ans))

        ans = Answer.objects.all()
        qs = Question.objects.all()
        qs2update = []
        for j in range(0, len(ans)):
            dig = qs.filter(id=ans[j].question_id.id).get().number_of_answers
            dig += 1
            qs.filter(id=ans[j].question_id.id).update(number_of_answers=dig)
            print(dig)
            # # Question.objects.by_id(ans[j].question_id.id).rating = dig
            # Question.objects.bulk_update(qs, ['number_of_answers'], batch_size=len(ans))
            # if (i + 1) % bulkBig == 0:
            #     Question.objects.bulk_update(qs, ['number_of_answers'], batch_size=bulkBig)
            #     qs = Question.objects.by_ids(question_ids[i:i+bulkBig])

    @staticmethod
    def check_in_list(search_list, key1, val1,key2, val2):
        for el in search_list:
            if el[key1] == val1 and el[key2] == val2:
                return False
        return True

    @staticmethod
    def fill_likes_dislikes_questions(like_and_dislike_count):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        likes_question = []
        q_ids = []
        p_ids = []
        for i in range(like_and_dislike_count):
            profile = Profile.objects.get(pk=choice(profile_ids))
            question = Question.objects.get(pk=choice(question_ids))
            places_p = find_el(p_ids, profile.id)
            places_q = find_el(q_ids, question.id)
            while not (len(places_p) == 0 or len(places_q) == 0) and find_dupl(places_p, places_q):
                profile = Profile.objects.get(pk=choice(profile_ids))
                question = Question.objects.get(pk=choice(question_ids))
                places_p = find_el(p_ids, profile.id)
                places_q = find_el(q_ids, question.id)
                print("REGENENERATE"+"!" * 10)

            p_ids.append(profile.id)
            q_ids.append(question.id)
            likes_question.append(LikeQuestion(
                profile_id=profile,
                question_id=question,
                is_like=faker.random.choice([True, False]))
            )
            print(likes_question[-1], i)
            if (i + 1) % bulkBig == 0:
                print("started creation  ", i)
                LikeQuestion.objects.bulk_create(likes_question[i+1 - bulkBig:i+1], bulkBig)
        if (i + 1) % bulkBig != 0:
            print("started creation  ")
            LikeQuestion.objects.bulk_create(likes_question[i - i%bulkBig:i+1],
                                             i%bulkBig + 1)

        #qs = Question.objects.by_ids(q_ids)
        qs = Question.objects.all()
        print(len(qs))
        for j in range(0, len(likes_question)):
            id = likes_question[j].question_id.id - 1
            print(id, "!"*100)
            dig = qs[id].rating
            dig += (1 if likes_question[j].is_like == True else 0)
            qs[id].rating = dig
            print(dig, " AND IS", qs[id].rating, j)
        Question.objects.bulk_update(qs, ['rating'], batch_size=len(qs))

    @staticmethod
    def fill_likes_dislikes_answers(like_and_dislike_count):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        answer_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )

        likes_answer = []
        a_ids = []
        p_ids = []
        profiles = Profile.objects.all()
        answers = Answer.objects.all()
        for i in range(like_and_dislike_count):
            profile = profiles.get(pk=choice(profile_ids))
            answer = answers.get(pk=choice(answer_ids))
            places_p = find_el(p_ids, profile.id)
            places_a = find_el(a_ids, answer.id)
            while not (len(places_p) == 0 or len(places_a) == 0) and find_dupl(places_p, places_a):
                profile = Profile.objects.get(pk=choice(profile_ids))
                answer = Answer.objects.get(pk=choice(answer_ids))
                places_p = find_el(p_ids, profile.id)
                places_a = find_el(a_ids, answer.id)
                print("REGENENERATE" + "!" * 10)

            p_ids.append(profile.id)
            a_ids.append(answer.id)
            likes_answer.append(LikeAnswer(
                profile_id=profile,
                answer_id=answer,
                is_like=faker.random.choice([True, False]))
            )
            print(likes_answer[-1], i)
            if (i + 1) % bulkBig == 0:
                print("started creation ", i)
                LikeAnswer.objects.bulk_create(likes_answer[i+1 - bulkBig:i+1], bulkBig)

        if (i + 1) % bulkBig != 0:
            print("started creation  ")
            LikeAnswer.objects.bulk_create(likes_answer[i - i%bulkBig:i+1],
                                             i%bulkBig + 1)

        ans = list(Answer.objects.all())
        for j in range(0, len(likes_answer)):
            id = likes_answer[j].answer_id.id - 1
            dig = ans[id].rating
            print("id ", id, " j ", j)
            dig += (1 if likes_answer[j].is_like == True else 0)
            ans[id].rating = dig
            ans[id].save()
            print(dig, " AND IS", ans[id].rating, j)
        #Question.objects.bulk_update(ans, ['rating'], batch_size=len(ans))

    def fill_db(self, ratios):
        print(ratios)
        self.fill_profiles(ratios['users'])
        print("tags")
        self.fill_tags(ratios['tags'])
        print("que")
        self.fill_questions(ratios['questions'])
        print("ans")
        self.fill_answers(ratios['answers'])
        print("votes")
        self.fill_likes_dislikes_questions(ratios['questionsVotes'])
        print("ans votes")
        self.fill_likes_dislikes_answers(ratios['answersVotes'])
        print("All done")
