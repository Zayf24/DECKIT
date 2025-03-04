# Generated by Django 5.1.6 on 2025-02-27 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flashcard', '0004_alter_deck_theme'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('total_questions', models.IntegerField()),
                ('correct_answers', models.IntegerField()),
                ('wrong_answers', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='flashcard.deck')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
