# Generated by Django 4.2.4 on 2023-08-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerund', '0007_question_answerable_question_answered'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='language_code',
            field=models.CharField(default='en', max_length=36),
        ),
    ]
