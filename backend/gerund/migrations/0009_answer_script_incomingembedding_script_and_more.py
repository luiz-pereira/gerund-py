# Generated by Django 4.2.5 on 2023-10-05 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerund', '0008_script_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='script',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='gerund.script'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incomingembedding',
            name='script',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_embeddings', to='gerund.script'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outgoingmessage',
            name='script',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_messages', to='gerund.script'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incomingembedding',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_embeddings', to='gerund.question'),
        ),
        migrations.AlterField(
            model_name='outgoingmessage',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_messages', to='gerund.answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='gerund.script'),
        ),
    ]
