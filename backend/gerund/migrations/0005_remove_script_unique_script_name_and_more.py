# Generated by Django 4.2.4 on 2023-08-28 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerund', '0004_script_name_script_unique_script_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='script',
            name='unique_script_name',
        ),
        migrations.AlterField(
            model_name='script',
            name='custom_prompt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='script',
            name='name',
            field=models.CharField(max_length=36, unique=True),
        ),
    ]
