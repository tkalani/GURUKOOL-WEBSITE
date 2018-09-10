from django.db import models
from django.contrib.auth.models import User

class GenderChoice(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False, unique=True)
	def __str__(self):
		return str(self.name)

class InstituteProfile(models.Model):
	institute_id = models.CharField(unique=True, null=False, blank=False, max_length=100)
	name = models.CharField(max_length=200)
	address_city = models.CharField(max_length=200)
	address_district = models.CharField(max_length=200)
	address_state = models.CharField(max_length=200)
	address_country = models.CharField(max_length=200)
	address_pincode = models.IntegerField(null=True, blank=True)
	email_address = models.CharField(max_length=100, null=False, blank=False)
	phone_no = models.CharField(max_length=100, null=False, blank=False)
	website = models.CharField(max_length=100, null=False, blank=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.institute_id) + ' --> ' + str(self.name)

class ProfessorAuthProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	mobile_no = models.IntegerField(blank=True, null=True)
	gender = models.ForeignKey(GenderChoice, on_delete=models.SET_NULL, null=True, blank=True)
	date_of_birth = models.DateField(blank=False, null=False)
	email_address = models.CharField(max_length=100, null=False, blank=False)

	email_verification_link = models.CharField(max_length=100, null=True, blank=True)
	email_verification_link_sent = models.BooleanField(default=False)
	email_verfied = models.BooleanField(default=False)
	otp = models.IntegerField(default=0)
	otp_sent_to_mobile_no = models.BooleanField(default=False)
	otp_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.username) + ' --> ' + str(self.user.id)

class StudentAuthProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	mobile_no = models.IntegerField(blank=True, null=True)
	gender = models.ForeignKey(GenderChoice, on_delete=models.SET_NULL, null=True, blank=True)
	date_of_birth = models.DateField(blank=False, null=False)
	email_address = models.CharField(max_length=100, null=False, blank=False)

	email_verification_link = models.CharField(max_length=100, null=True, blank=True)
	email_verification_link_sent = models.BooleanField(default=False)
	email_verfied = models.BooleanField(default=False)
	otp = models.IntegerField(default=0)
	otp_sent_to_mobile_no = models.BooleanField(default=False)
	otp_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.username) + ' --> ' + str(self.user.id)