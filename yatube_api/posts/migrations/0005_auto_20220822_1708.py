# Generated by Django 3.2.15 on 2022-08-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_follow_unique_name_userr'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_name_userr',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('following', 'user'), name='unique_following_user'),
        ),
    ]
