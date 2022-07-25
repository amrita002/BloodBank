# Generated by Django 2.2 on 2019-04-27 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blood_bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=30)),
                ('a_positive', models.IntegerField(default=0)),
                ('b_positive', models.IntegerField(default=0)),
                ('ab_positive', models.IntegerField(default=0)),
                ('o_positive', models.IntegerField(default=0)),
                ('a_negative', models.IntegerField(default=0)),
                ('b_negative', models.IntegerField(default=0)),
                ('ab_negative', models.IntegerField(default=0)),
                ('o_negative', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Blood_bank',
            },
        ),
        migrations.CreateModel(
            name='Blood_seek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
                ('group', models.CharField(default='', max_length=10)),
                ('units', models.IntegerField()),
                ('location', models.CharField(max_length=20)),
                ('status', models.CharField(default='not yet approved', max_length=50)),
                ('role', models.CharField(default='', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Blood_seek',
            },
        ),
        migrations.CreateModel(
            name='Donor_reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30)),
                ('user_location', models.CharField(blank=True, max_length=30, null=True)),
                ('mail', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
                ('group', models.CharField(max_length=20)),
                ('bp', models.CharField(default=None, max_length=6)),
                ('diabetes', models.CharField(default='no', max_length=3)),
                ('physical_disorders', models.CharField(default='no', max_length=3)),
                ('diease', models.CharField(default='no', max_length=20)),
                ('status', models.CharField(default='not yet approved', max_length=50)),
                ('units', models.IntegerField(default=0)),
                ('date', models.DateField(blank=True, null=True)),
                ('bol', models.CharField(default='latest', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Donor_reports',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('user_mail', models.EmailField(max_length=254)),
                ('user_pass', models.CharField(max_length=20)),
                ('user_role', models.CharField(max_length=10)),
                ('user_phone_number', models.CharField(default='0000000000', max_length=10)),
                ('user_address', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
    ]
