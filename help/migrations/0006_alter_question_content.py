# Generated by Django 4.2.16 on 2025-02-25 14:39

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0005_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Текст вопроса'),
        ),
    ]
