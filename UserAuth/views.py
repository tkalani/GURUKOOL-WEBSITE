from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from django.core.urlresolvers import reverse
from .models import *
from communications import *
from django.core import mail
from random import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from Student.models import *
from Professor.models import *

def landingPage(request):
	if request.method == 'GET':
		print('wfwfw')
		if request.user.is_authenticated:
			print('here now now')
			if request.user.groups.filter(name='Professor').exists():
				print('professor')
				return HttpResponseRedirect(reverse('Professor:dashboard'))
			elif request.user.groups.filter(name='Student').exists():
				print('stuednt')
				return HttpResponseRedirect(reverse('Student:dashboard'))
		return render(request, 'UserAuth/landingPage.html')

def loginUser(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			if request.user.groups.filter(name='Professor').exists():
				return HttpResponseRedirect(reverse('Professor:dashboard'))
			elif request.user.groups.filter(name='Student').exists():
				return HttpResponseRedirect(reverse('Student:dashboard'))
		return render(request, 'UserAuth/loginPage.html')

def signupUser(request):
	if request.method == 'GET':
		if request.user.is_authernticated:
			if request.user.groups.filter(name='Professor').exists():
				return HttpResponseRedirect(reverse('Professor:dashboard'))
			elif request.user.groups.filter(name='Student').exists():
				return HttpResponseRedirect(reverse('Student:dashboard'))
		gender_choices = GenderChoice.objects.all()
		return render(request, 'UserAuth/signupPage.html', {'gender_choices': gender_choices})

def signupProfessor(request):
	if request.method == 'POST':
		first_name = request.POST.get('professor_signup_first_name')
		middle_name = request.POST.get('professor_signup_middle_name')
		last_name = request.POST.get('professor_signup_last_name')
		email = request.POST.get('professor_signup_email')
		mobile_no = request.POST.get('professor_signup_mobile_no')
		date_of_birth = request.POST.get('professor_signup_date_of_birth')
		gender = request.POST.get('professor_signup_gender')
		password = request.POST.get('professor_signup_password')

		otp = randint(100000, 999999)

		if User.objects.filter(is_superuser=False, email=email).count() > 0 or ProfessorAuthProfile.objects.filter(mobile_no=mobile_no).count() > 0 or StudentAuthProfile.objects.filter(mobile_no=mobile_no).count() > 0:
			return HttpResponse('user already signed up with this mobile no or email')
		else:
			gender = GenderChoice.objects.get(name=gender)

			user_instance = User()
			user_instance.username = email
			user_instance.first_name = first_name
			user_instance.middle_name = middle_name
			user_instance.last_name = last_name
			user_instance.email = email
			user_instance.set_password(password)
			user_instance.save()

			group = Group.objects.get(name='Professor')
			group.user_set.add(user_instance)

			professor_auth_profile_instance = ProfessorAuthProfile()
			professor_auth_profile_instance.user = user_instance
			professor_auth_profile_instance.mobile_no = mobile_no
			professor_auth_profile_instance.date_of_birth = date_of_birth
			professor_auth_profile_instance.gender = gender
			professor_auth_profile_instance.email_address = email
			professor_auth_profile_instance.otp = otp
			professor_auth_profile_instance.save()

			professor_profile_instance = ProfessorProfile()
			professor_profile_instance.user = professor_auth_profile_instance
			professor_profile_instance.mobile_no = mobile_no
			professor_profile_instance.date_of_birth = date_of_birth
			professor_profile_instance.gender = gender
			professor_profile_instance.save()

			user = authenticate(username=email, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('Professor:dashboard'))
	return HttpResponse('professor signup')

def signupStudent(request):
	if request.method == 'POST':
		first_name = request.POST.get('student_signup_first_name')
		middle_name = request.POST.get('student_signup_middle_name')
		last_name = request.POST.get('student_signup_last_name')
		email = request.POST.get('student_signup_email')
		mobile_no = request.POST.get('student_signup_mobile_no')
		date_of_birth = request.POST.get('student_signup_date_of_birth')
		gender = request.POST.get('student_signup_gender')
		password = request.POST.get('student_signup_password')

		otp = randint(100000, 999999)

		if User.objects.filter(is_superuser=False, email=email).count() > 0 or ProfessorAuthProfile.objects.filter(mobile_no=mobile_no).count() > 0 or StudentAuthProfile.objects.filter(mobile_no=mobile_no).count() > 0:
			return HttpResponse('user already signed up with this mobile no or email')
		else:
			gender = GenderChoice.objects.get(name=gender)

			user_instance = User()
			user_instance.username = email
			user_instance.first_name = first_name
			user_instance.middle_name = middle_name
			user_instance.last_name = last_name
			user_instance.email = email
			user_instance.set_password(password)
			user_instance.save()

			group = Group.objects.get(name='Student')
			group.user_set.add(user_instance)

			student_auth_profile_instance = StudentAuthProfile()
			student_auth_profile_instance.user = user_instance
			student_auth_profile_instance.mobile_no = mobile_no
			student_auth_profile_instance.date_of_birth = date_of_birth
			student_auth_profile_instance.gender = gender
			student_auth_profile_instance.email_address = email
			student_auth_profile_instance.otp = otp
			student_auth_profile_instance.save()

			student_profile_instance = StudentProfile()
			student_profile_instance.user = student_auth_profile_instance
			student_profile_instance.mobile_no = mobile_no
			student_profile_instance.date_of_birth = date_of_birth
			student_profile_instance.gender = gender
			student_profile_instance.save()

			user = authenticate(username=email, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('Student:dashboard'))
	return HttpResponse('student signup')