# Generated by Django 4.1.3 on 2022-11-16 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_init_portfolio_db'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='datetime',
        ),
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]