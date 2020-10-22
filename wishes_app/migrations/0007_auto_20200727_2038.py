# Generated by Django 2.2.4 on 2020-07-28 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishes_app', '0006_wish_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='grant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wish',
            name='wishers_who_liked',
            field=models.ManyToManyField(related_name='granted_wishes_liked', to='wishes_app.User'),
        ),
    ]
