# Generated by Django 5.1.6 on 2025-02-21 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='last_accessed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
