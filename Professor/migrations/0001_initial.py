# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-05 15:20
from __future__ import unicode_literals

import Professor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.IntegerField(blank=True, null=True)),
                ('date_of_birth', models.DateField()),
                ('address_city', models.CharField(max_length=200)),
                ('address_district', models.CharField(max_length=200)),
                ('address_state', models.CharField(max_length=200)),
                ('address_country', models.CharField(max_length=200)),
                ('address_pincode', models.IntegerField()),
                ('profile_pic', models.ImageField(blank=True, default='/PROFESSOR-PROFILE-PIC-DIRECTORY/professor_avatar.png', null=True, upload_to=Professor.models.get_professor_profile_pic_path)),
                ('qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('email_address_verified', models.BooleanField(default=False)),
                ('mobile_no_address_verified', models.BooleanField(default=False)),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserAuth.GenderChoice')),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserAuth.InstituteProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ProfessorProf', to='UserAuth.ProfessorAuthProfile')),
            ],
        ),
    ]
