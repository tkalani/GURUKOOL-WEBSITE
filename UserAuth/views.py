import string
import re
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
from django.contrib import messages
from django.views import View
from .utils import *
from django.contrib.auth.decorators import login_required
from django.conf import settings

SHOW_MESSAGE_URL = 'UserAuth:show-message'
EMAIL_VERIFICATION_LINK_LENGTH = 50
LOGIN_URL = 'UserAuth:landingPage'

def redirectPage(request, user_token):
	'''
		Redirects the page
		Takes input request method and user_token
		returns http response
	'''
	request.session['token'] = user_token
	return HttpResponseRedirect(reverse('Student:dashboard'))
	
class landingPage(View):
	'''
	get Landing Page
	'''
	get_login_page = 'UserAuth/landingPage.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.groups.filter(name='Professor').exists():
				return HttpResponseRedirect(reverse('Professor:dashboard'))
			elif request.user.groups.filter(name='Student').exists():
				return HttpResponseRedirect(reverse('Student:dashboard'))
		return render(request, self.get_login_page)

class Login(View):
	get_login_template = 'UserAuth/loginPage.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.groups.filter(name='Professor').exists():
				return HttpResponseRedirect(reverse('Professor:dashboard'))
			elif request.user.groups.filter(name='Student').exists():
				return HttpResponseRedirect(reverse('Student:dashboard'))
		return render(request, self.get_login_template)

	def post(self, request, *args, **kwargs):
		messages.error(request, 'BAD REQUEST')
		return HttpResponseRedirect(reverse(settings.MESSAGE_URL))

class LoginUser(View):
	def post(self, request, *args, **kwargs):
		try:
			type_of_user = kwargs.get('type', None)
			if type_of_user == 'professor':
				username = request.POST.get('professor_login_username')
				password = request.POST.get('professor_login_password')

				if username.isdigit():
					try:
						instance = ProfessorAuthProfile.objects.filter(mobile_no=username)
						if len(instance) > 1:
							message = 'More than one account is registered with this mobile number.  Kindly use Email-ID to login.'
							messages.warning(request, message)
							return HttpResponseRedirect(reverse('UserAuth:login'))
						else:
							instance = instance[0]
						username = instance.user.username
						user = authenticate(username=username, password=password)
						if user is not None:
							login(request, user)
							return HttpResponseRedirect(reverse('Professor:dashboard'))
						messages.warning(request, "Phone No and password doesn't match with any GURUKOOL PROFESSOR account.")
						return HttpResponseRedirect(reverse('UserAuth:login'))
					except:
						messages.warning(request, "No GURUKOOL PROFESSOR account is registered with that mobile no.")
						return HttpResponseRedirect(reverse('UserAuth:login'))
				else:
					try:
						match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', username)
						if match is None:
							messages.warning(request, 'E-mail entered is not a valid email-address')
							return HttpResponseRedirect(reverse('UserAuth:login'))
						try:
							instance = ProfessorAuthProfile.objects.get(email_address=username)
						except:
							messages.warning(request, 'No GURUKOOL PROFESSOR account registered with this email-address.')
							return HttpResponseRedirect(reverse('UserAuth:login'))
						user = authenticate(username=username, password=password)
						if user is not None:
							login(request, user)
							return HttpResponseRedirect(reverse('Student:dashboard'))
						messages.warning(request, "Email address and Password does not match to any GURUKOOL PROFESSOR Account.")
						return HttpResponseRedirect(reverse('UserAuth:login'))
					except:
						messages.error(request, 'BAD REQUEST')
						return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
			elif type_of_user == 'student':
				if request.method == 'POST':
					username = request.POST.get('student_login_username')
					password = request.POST.get('student_login_password')

					if username.isdigit():
						try:
							instance = ProfessorAuthProfile.objects.filter(mobile_no=username)
							if len(instance) > 1:
								message = 'More than one account is registered with this mobile number.  Kindly use Email-ID to login.'
								messages.warning(request, message)
								return HttpResponseRedirect(reverse('UserAuth:login'))
							else:
								instance = instance[0]
							username = instance.user.username
							user = authenticate(username=username, password=password)
							if user is not None:
								login(request, user)
								return HttpResponseRedirect(reverse('Student:dashboard'))
							messages.warning(request, "Phone No and password doesn't match with any GURUKOOL STUDENT account.")
							return HttpResponseRedirect(reverse('UserAuth:login'))
						except:
							messages.warning(request, "No GURUKOOL STUDENT account is registered with that mobile no.")
							return HttpResponseRedirect(reverse('UserAuth:login'))
					else:
						try:
							match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', username)
							if match is None:
								messages.warning(request, 'E-mail entered is not a valid email-address')
								return HttpResponseRedirect(reverse('UserAuth:login'))
							try:
								instance = StudentAuthProfile.objects.get(email_address=username)
							except:
								messages.warning(request, 'No GURUKOOL STUDENT account registered with this email-address.')
								return HttpResponseRedirect(reverse('UserAuth:login'))
							user = authenticate(username=username, password=password)
							if user is not None:
								login(request, user)
								return HttpResponseRedirect(reverse('Student:dashboard'))
							messages.warning(request, "Email address and Password does not match to any GURUKOOL STUDENT Account")
							return HttpResponseRedirect(reverse('UserAuth:login'))
						except:
							messages.error(request, 'BAD REQUEST')
							return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
				else:
					messages.error(request, 'BAD REQUEST')
					return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
			else:
				messages.error(request, 'BAD REQUEST')
				return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
		except Exception as e:
			print(e)
			messages.error(request, 'BAD REQUEST')
			return HttpResponseRedirect(reverse(settings.MESSAGE_URL))


class SignUp(View):
	get_signup_template = 'UserAuth/signupPage.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.groups.filter(name='Professor').exists():
				return HttpResponseRedirect(reverse('Professor:dashboard'))
			elif request.user.groups.filter(name='Student').exists():
				return HttpResponseRedirect(reverse('Student:dashboard'))
		gender_choices = GenderChoice.objects.all()
		return render(request, self.get_signup_template, {'gender_choices': gender_choices})

	def post(self, request, *args, **kwargs):
		messages.error(request, 'BAD REQUEST')
		return HttpResponseRedirect(reverse(settings.MESSAGE_URL))

class signupUser(View):
	def get(self, request, *args, **kwargs):
		messages.error(request, 'BAD REQUEST')
		return HttpResponseRedirect(reverse(settings.MESSAGE_URL))

	def post(self, request, *args, **kwargs):
		try:
			type_of_user = kwargs.get('type', None)

			if type_of_user == 'professor':
				first_name = request.POST.get('professor_signup_first_name')
				middle_name = request.POST.get('professor_signup_middle_name')
				last_name = request.POST.get('professor_signup_last_name')
				email = request.POST.get('professor_signup_email')
				mobile_no = request.POST.get('professor_signup_mobile_no')
				date_of_birth = request.POST.get('professor_signup_date_of_birth')
				gender = request.POST.get('professor_signup_gender')
				password = request.POST.get('professor_signup_password')

				otp = randint(100000, 999999)
				email_verification_link = ''.join([choice(string.ascii_letters + string.digits) for n in range(EMAIL_VERIFICATION_LINK_LENGTH)])

				if User.objects.filter(is_superuser=False, email=email).count() > 0:
					messages.warning(request, 'user already signed up with this email')
					return HttpResponseRedirect(reverse('UserAuth:signup'))
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
					professor_auth_profile_instance.email_verification_link = email_verification_link
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
					messages.error(request, 'BAD REQUEST')
					return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
			elif type_of_user == 'student':
				first_name = request.POST.get('student_signup_first_name')
				middle_name = request.POST.get('student_signup_middle_name')
				last_name = request.POST.get('student_signup_last_name')
				email = request.POST.get('student_signup_email')
				mobile_no = request.POST.get('student_signup_mobile_no')
				date_of_birth = request.POST.get('student_signup_date_of_birth')
				gender = request.POST.get('student_signup_gender')
				password = request.POST.get('student_signup_password')

				otp = randint(100000, 999999)
				email_verification_link = ''.join([choice(string.ascii_letters + string.digits) for n in range(EMAIL_VERIFICATION_LINK_LENGTH)])

				if User.objects.filter(is_superuser=False, email=email).count() > 0:
					messages.warning(request, 'user already signed up with this email')
					return HttpResponseRedirect(reverse('UserAuth:signup'))
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
					student_auth_profile_instance.email_verification_link = email_verification_link
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
					messages.error(request, 'BAD REQUEST')
					return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
			else:
				messages.error(request, 'BAD REQUEST')
				return HttpResponseRedirect(reverse(settings.MESSAGE_URL))
		except Exception as e:
			messages.error(request, 'BAD REQUEST')
			return HttpResponseRedirect(reverse(settings.MESSAGE_URL))

@login_required(login_url=LOGIN_URL)
def send_verification_data(request, user_group, send_to):
	# if request.user.groups.filter(name=user_group).exists():
	# 	try:
	# 		verification_link = ProfessorAuthProfile.objects.get(user__username=request.user).email_verification_link
	# 		subject = 'GURUKOOL ACCOUNT VERIFICATION'
	# 		# body = 'Verify your GURUKOOL %s ACCOUNT.\nVerify Account Here.\n\n %s' %(user_group, verification_link)
	# 		body = 'SCNKSJNCSJKDC'
	# 		recipient = request.user.email
	# 		print(request, recipient, subject, body, None)
	# 		sendEmail(request, recipient, subject, body, None)
	# 	except Exception as e:
	# 		print(e)
	# 		messages.error(request, 'EMAIL NOT SENT. PLEASE TRY LATER')
	# 		if user_group == 'Professor':
	# 			return HttpResponseRedirect(reverse('Professor:dashboard'))
	# 		elif user_group == 'Student':
	# 			return HttpResponseRedirect(reverse('Student:dashboard'))
	# else:
	# 	messages.error(request, 'EMAIL NOT SENT. PLEASE TRY LATER')
	# 	if user_group == 'Professor':
	# 		return HttpResponseRedirect(reverse('Professor:dashboard'))
	# 	elif user_group == 'Student':
	# 		return HttpResponseRedirect(reverse('Student:dashboard'))
	sendEmail(request, 'tanmay.k16@iiits.in', 'sbdcnsbcmsc', 'asbcnsc nsdc ', None)
