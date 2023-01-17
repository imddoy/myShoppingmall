# Generated by Django 4.1.3 on 2022-12-17 07:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_remove_item_like_users_item_like_item_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='like',
        ),
        migrations.RemoveField(
            model_name='item',
            name='like_count',
        ),
        migrations.AddField(
            model_name='item',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]