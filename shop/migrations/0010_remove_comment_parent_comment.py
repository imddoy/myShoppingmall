# Generated by Django 3.2 on 2022-12-18 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_comment_parent_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent_comment',
        ),
    ]