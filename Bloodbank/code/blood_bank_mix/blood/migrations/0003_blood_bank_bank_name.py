# Generated by Django 2.2 on 2019-04-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0002_users_user_main_branch_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_bank',
            name='bank_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]