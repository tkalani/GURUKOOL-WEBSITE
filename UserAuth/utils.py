from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse

def show_message(request):
	return render(request, 'UserAuth/message.html')

def is_user_verfied(request):
	inst = None
	if request.user.groups.filter(name='Professor').exists():
		try:
			inst = ProfessorAuthProfile.objects.get(user__username=request.user)
		except Exception as e:
			return False
	elif request.user.groups.filter(name='Student').exists():
		try:
			inst = ProfessorAuthProfile.objects.get(user__username=request.user)
		except Exception as e:
			return False
	else:
		return False
	if inst.email_verified or inst.otp_verified:
		return True
	return False