# Generated by Django 4.2.4 on 2023-08-29 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerund', '0005_remove_script_unique_script_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gerund.question'),
        ),
    ]
