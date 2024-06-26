# Generated by Django 4.2.4 on 2023-08-23 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerund', '0003_script_rename_incomingembeddings_incomingembedding_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='name',
            field=models.CharField(max_length=36, null=True),
        ),
        migrations.AddConstraint(
            model_name='script',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_script_name'),
        ),
    ]
