from django.test import TestCase
from django.test.client import Client
from Student.models import *
from UserAuth.models import *
from Professor.models import *
from .models import Meeting
import datetime

class MeetingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.client = Client()
        cls.user = User.objects.create_user('test@gmail.com', 'test@gmail.com', 'testpassword')
        cls.user1 = User.objects.create_user('test1@gmail.com', 'test1@gmail.com', 'testpassword')
        gender=GenderChoice.objects.create(name='Male')
        student=StudentAuthProfile.objects.create(user=cls.user,mobile_no='123568966',gender=gender,date_of_birth=datetime.date.today, email_address='test@gmail.com')
        s_profile=StudentProfile.objects.create(user=student,date_of_birth=datetime.date.today)
        professor=ProfessorAuthProfile.objects.create(user=cls.user1,mobile_no='123568966',gender=gender,date_of_birth=datetime.date.today, email_address='test1@gmail.com')
        p_profile=ProfessorProfile.objects.create(user=professor,date_of_birth=datetime.date.today)
        Meeting.objects.create(student=s_profile, professor=p_profile, title="Meeting Test", body="This is a Test")

    def test_title_label(self):
        meeting = Meeting.objects.get(id=1)
        field_label = author._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Meeting Test')

    def test_body_label(self):
        meeting = Meeting.objects.get(id=1)
        field_label = author._meta.get_field('body').verbose_name
        self.assertEquals(field_label, 'This is a Test')
