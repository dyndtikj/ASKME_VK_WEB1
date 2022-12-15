import django

from django.forms import  TextInput,  Textarea, FileInput
from django.contrib.auth.models import User
from app.models import *
from django.forms import PasswordInput
from django.contrib.auth.password_validation import validate_password
from django import forms


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(
                attrs={'class': 'form-control',
                       'maxlength': 100,
                       'placeholder': 'My_NiCkNaMe55',
                       'required': True,
                       'id': 'username-input',
                       'required pattern': '^[-a-zA-Z0-9_+.@]+$'}),
            'password': PasswordInput(
                attrs={'class': 'form-control',
                       'maxlength': 100,
                       'placeholder': 'My_NiCkNaMe55',
                       'required': True,
                       'id': 'password-input',
                       'required pattern': '^(?=.*\d)(?=.*[A-Z]).{8,}$',
                       })
        }

        labels = {
            'username': 'Login',
            'password': 'Password'
        }

    def clean(self):
        pass


class SignupForm(forms.ModelForm):
    repeat_password = forms.CharField(required=True,
                                      widget=PasswordInput(attrs={
                                          'type': 'password',
                                          'class': 'form-control',
                                          'maxlength': 100,
                                          'placeholder': 'My_NiCkNaMe55',
                                          'id': 'repeat-password-input',
                                          'required pattern': '^(?=.*\d)(?=.*[A-Z]).{8,}$',
                                      }),
                                      label='Repeat password ')

    avatar = forms.FileField(required=True,
                             widget=FileInput(attrs={
                                 'class': 'form-control',
                                 'id': 'avatar-input',
                                 'type': 'file',
                                 'name': 'avatar',
                                 'accept': 'image/*',
                             }),
                             label='Avatar')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': TextInput(
                attrs={'class': 'form-control',
                       'maxlength': 100,
                       'placeholder': 'My_NiCkNaMe55',
                       'required': True,
                       'id': 'username-input',
                       'required pattern': '^[-a-zA-Z0-9_+.@]+$'}),
            'password': PasswordInput(
                attrs={'class': 'form-control',
                       'maxlength': 100,
                       'type': 'password',
                       'placeholder': 'My_NiCkNaMe55',
                       'required': True,
                       'id': 'password-input',
                       'required pattern': '^(?=.*\d)(?=.*[A-Z]).{8,}$'}),
            'email': TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'required': True,
                'id': 'email-input',
                'placeholder': 'name@example.com',
                'type': 'email',
            }),
        }

        labels = {
            'username': 'Login',
            'password': 'Password',
            'email': 'Email',
        }

    def clean(self):
        pass

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', 'This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            print("email in use")
            self.add_error('email', 'This email is already in use')
            return ""
        return self.cleaned_data['email']

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if not password or not repeat_password:
            return password
        if password != repeat_password:
            self.add_error('repeat_password', 'Passwords do not match!')
            return ""

        try:
            django.contrib.auth.password_validation.validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password', 'Invalid password. it must contain one upper and one lowercase letter and at '
                                       'least one number and be 8-100 characters long')
            return ""
        return password

    def save(self, **kwargs):
        print("saving...")
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)

        profile = Profile.objects.create(user_id=user)
        if self.cleaned_data['avatar'] is not None:
            profile.avatar = self.cleaned_data['avatar']
            profile.save()

        return user


class SettingsForm(forms.Form):
    repeat_password = forms.CharField(required=False,
                                      empty_value="111",
                                      widget=PasswordInput(attrs={
                                          'type': 'password',
                                          'class': 'form-control',
                                          'maxlength': 100,
                                          'placeholder': 'My_NiCkNaMe55',
                                          'id': 'repeat-password-input',
                                      }),
                                      label='Repeat password',
                                      )

    username = forms.CharField(required=False,
                               widget=TextInput(
                                   attrs={'class': 'form-control',
                                          'maxlength': 100,
                                          'placeholder': 'My_NiCkNaMe55',
                                          'required': False,
                                          'id': 'username-input',
                                          'value': '{{ user.username }}',
                                          }),
                               label='Login'
                               )
    email = forms.EmailField(required=False,
                             widget=TextInput(attrs={
                                 'class': 'form-control',
                                 'maxlength': 100,
                                 'required': False,
                                 'id': 'email-input',
                                 'placeholder': 'name@example.com',
                                 'type': 'email',
                                 'value': '{{user.email}}',
                             }),
                             label='Email',
                             )

    password = forms.CharField(required=False,
                               widget=PasswordInput(attrs={
                                   'type': 'password',
                                   'class': 'form-control',
                                   'maxlength': 100,
                                   'placeholder': 'My_NiCkNaMe55',
                                   'id': 'password-input',
                               }),
                               label='Password',
                               )

    avatar = forms.FileField(required=False,
                             widget=FileInput(attrs={
                                 'class': 'form-control',
                                 'id': 'avatar-input',
                                 'type': 'file',
                                 'name': 'avatar',
                                 'accept': 'image/*',
                             }),
                             label='Avatar')

    def __init__(self, user=None, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(**kwargs)

    def clean_username(self):
        if not self.cleaned_data['username']:
            return self.cleaned_data['username']
        if self.user.username != self.cleaned_data['username']:
            if User.objects.filter(username=self.cleaned_data['username']).exists():
                self.add_error(None, 'This username is already in use')
                raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if not self.cleaned_data['email']:
            return self.user.email
        if self.user.email != self.cleaned_data['email']:
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error(None, 'This email is already in use')
                raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']

    def clean_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if not password or not repeat_password:
            return password
        if password != repeat_password:
            self.add_error('password', 'Passwords do not match!')
            return ""

        try:
            django.contrib.auth.password_validation.validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password', 'Invalid password. it must contain one upper and one lowercase letter and at '
                                       'least one number and be 8-100 characters long')
            return ""
        return password

    def save(self, **kwargs):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            self.user.set_password(self.cleaned_data['password'])

        self.user.save()

        profile = Profile.objects.get(user_id=self.user)
        if self.cleaned_data['avatar'] is not None:
            profile.avatar = self.cleaned_data['avatar']
            profile.save()

        return self.user


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=True,
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control is-valid m-0',
                               'placeholder': 'food cooking chocolate',
                               'type': 'text',
                               'title': 'maximum length 200 characters, it cannot be empty',
                               'pattern': '^(\s*[a-zA-Z]+[\w\-\d]*\s*)+$',
                               'id': 'tags-input',
                           }),
                           label='Tags')

    class Meta:
        model = Question
        fields = ['title', 'text']

        widgets = {
            'title': TextInput(attrs={
                'type': 'text',
                'class': 'form-control is-valid m-0',
                'id': 'question',
                'name': 'new_question',
                'placeholder': 'How are you?',
                'maxlength': 150,
                'title': 'maximum length 200 characters, it cannot be empty',
                'pattern': '^(\s*[\w\p{P}]+\s*)+$',
            }),

            'text': Textarea(attrs={
                'class': 'form-control m-0 is-invalid',
                'id': 'question-body',
                'placeholder': 'enter more details here...',
                'maxlength': 1000,
                'title': 'maximum length 300 characters, it cannot be empty',
                'rows': '7',
            }),
        }

        labels = {
            'title': 'Your question',
            'text': 'More details',
        }

    def __init__(self, author=None, **kwargs):
        self._author = author
        super(AskForm, self).__init__(**kwargs)

    def clean_tags(self):
        self.tags = self.cleaned_data['tags'].split()
        if len(self.tags) > 25:
            self.add_error(None, 'Use no more than 25 tags')
            raise forms.ValidationError('Use no more than 25 tags')
        return self.tags

    def save(self, **kwargs):
        published_question = Question()
        published_question.profile_id = self._author
        published_question.title = self.cleaned_data['title']
        published_question.text = self.cleaned_data['text']
        published_question.save()

        for tag in self.tags:
            if not Tag.objects.filter(tag=tag).exists():
                Tag.objects.create(tag=tag)
        published_question.tags.set(Tag.objects.create_question(self.tags))

        return published_question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control m-0 is-invalid',
                'id': 'input-answer',
                'placeholder': 'enter your answer here...',
                'maxlength': 1000,
                'title': 'maximum length 300 characters, the answer cannot be empty',
                'rows': '3',
                'required': True,
            }),
        }

        labels = {
            'text': 'More details',
        }

    def save(self, **kwags):
        published_answer = Answer()
        published_answer.profile_id = self._author
        published_answer.text = self.cleaned_data['text']
        published_answer.save()

        return published_answer

# from django import forms
#
# from django.forms import ModelForm, TextInput, PasswordInput, DateTimeInput, Textarea, FileInput
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from app.models import *
# from django.forms import PasswordInput
#
#
# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = {
#             'username': TextInput(
#                 attrs={'class': 'form-control',
#                        'maxlength': 100,
#                        'placeholder': 'My_NiCkNaMe55',
#                        'required': True,
#                        'id': 'username-input',
#                        'required pattern': '^[-a-zA-Z0-9_+.@]+$'}),
#             'password': PasswordInput(
#                 attrs={'class': 'form-control',
#                        'maxlength': 100,
#                        'placeholder': 'My_NiCkNaMe55',
#                        'required': True,
#                        'id': 'password-input',
#                        'required pattern': '^(?=.*\d)(?=.*[A-Z]).{8,}$'})
#         }
#
#         labels = {
#             'username': 'Login',
#             'password': 'Password'
#         }
#
#     def clean(self):
#         pass
#
#     # def clean_username(self):
#     #     print('34')
#     #     return
#
#
# class SignupForm(forms.ModelForm):
#     repeat_password = forms.CharField(required=True,
#                                       widget=PasswordInput(attrs={
#                                           'type': 'password',
#                                           'class': 'form-control',
#                                           'maxlength': 100,
#                                           'placeholder': 'My_NiCkNaMe55',
#                                           'id': 'repeat-password-input',
#                                           'required pattern': '^(?=.*\d)(?=.*[A-Z]).{8,}$',
#                                       }),
#                                       label='Password check')
#
#     avatar = forms.FileField(required=True,
#                              widget=FileInput(attrs={
#                                  'class': 'form-control',
#                                  'id': 'avatar-input',
#                                  'type': 'file',
#                                  'name': 'avatar',
#                                  'accept': 'image/*',
#                              }),
#                              label='Avatar')
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#
#         widgets = {
#             'username': TextInput(
#                 attrs={'class': 'form-control',
#                        'maxlength': 100,
#                        'placeholder': 'My_NiCkNaMe55',
#                        'required': True,
#                        'id': 'username-input',
#                        'required pattern': '^[-a-zA-Z0-9_+.@]+$'}),
#             'password': PasswordInput(
#                 attrs={'class': 'form-control',
#                        'maxlength': 100,
#                        'type': 'password',
#                        'placeholder': 'My_NiCkNaMe55',
#                        'required': True,
#                        'id': 'password-input',
#                        'required pattern': '^(?=.*\d)(?=.*[A-Z]).{8,}$'}),
#             'email': TextInput(attrs={
#                 'class': 'form-control',
#                 'maxlength': 100,
#                 'required': True,
#                 'id': 'email-input',
#                 'placeholder': 'name@example.com',
#                 'type': 'email',
#             }),
#         }
#
#         labels = {
#             'username': 'Login',
#             'password': 'Password',
#             'email': 'Email',
#         }
#
#     def clean(self):
#         if not 'password' in self.cleaned_data or not 'repeat_password' in self.cleaned_data:
#             raise forms.ValidationError('Password is too short (minimum 1 characters)')
#         if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
#             self.add_error('password', 'Passwords do not match!')
#             self.add_error('repeat_password', 'Passwords do not match!')
#             raise forms.ValidationError('Passwords do not match!')
#
#     def clean_username(self):
#         if User.objects.filter(username=self.cleaned_data['username']).exists():
#             self.add_error(None, 'This username is already in use')
#             raise forms.ValidationError('This username is already in use')
#         return self.cleaned_data['username']
#
#     def clean_email(self):
#         if User.objects.filter(email=self.cleaned_data['email']).exists():
#             self.add_error(None, 'This email is already in use')
#             raise forms.ValidationError('This email is already in use')
#         return self.cleaned_data['email']
#
#     def save(self, **kwargs):
#         username = self.cleaned_data['username']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#         user = User.objects.create_user(username, email, password)
#
#         profile = Profile.objects.create(user_id=user)
#         if self.cleaned_data['avatar'] is not None:
#             profile.avatar = self.cleaned_data['avatar']
#             profile.save()
#
#         return user