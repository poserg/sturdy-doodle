# Generated by Django 4.1.3 on 2022-11-16 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_increase_accurancy_moneyfield'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='amount',
            new_name='lots',
        ),
    ]