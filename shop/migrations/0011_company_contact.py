# Generated by Django 3.2 on 2022-12-19 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_comment_parent_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.CharField(default=1, max_length=12),
            preserve_default=False,
        ),
    ]
