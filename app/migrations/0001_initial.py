# Generated by Django 4.1.3 on 2022-11-15 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='uploads/avatar/ava.png', upload_to='static/avatar/', verbose_name='Avatar')),
                ('user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32, unique=True, verbose_name='Tag')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('number_of_answers', models.IntegerField(default=0, verbose_name='Answer count')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('likes_count', models.IntegerField(default=0, verbose_name='Likes')),
                ('dislikes_count', models.IntegerField(default=0, verbose_name='Dislikes')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Author')),
                ('tags', models.ManyToManyField(to='app.tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is correct')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('likes_count', models.IntegerField(default=0, verbose_name='Likes')),
                ('dislikes_count', models.IntegerField(default=0, verbose_name='Dislikes')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Author')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='LikeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True, verbose_name='Like or dislike')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Profile')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Question like',
                'verbose_name_plural': 'Question likes',
                'unique_together': {('question_id', 'profile_id')},
            },
        ),
        migrations.CreateModel(
            name='LikeAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=True, verbose_name='Like or dislike')),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer', verbose_name='Answer')),
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Answer like',
                'verbose_name_plural': 'Answers likes',
                'unique_together': {('answer_id', 'profile_id')},
            },
        ),
    ]
