# Generated by Django 2.2 on 2019-04-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0004_auto_20190427_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_bank',
            name='user_main_branch_name',
            field=models.CharField(default='main', max_length=20),
        ),
        migrations.AlterField(
            model_name='blood_bank',
            name='location',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='blood_seek',
            name='location',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='donor_reports',
            name='location',
            field=models.CharField(default='', max_length=30),
        ),
    ]