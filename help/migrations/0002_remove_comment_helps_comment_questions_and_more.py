# Generated by Django 4.2.16 on 2025-02-14 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('help', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='helps',
        ),
        migrations.AddField(
            model_name='comment',
            name='questions',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comment_question', to='help.question'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_question', to=settings.AUTH_USER_MODEL),
        ),
    ]
