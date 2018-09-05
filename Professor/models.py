from django.db import models
from django.contrib.auth.models import User
from UserAuth.models import *

def get_professor_profile_pic_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (instance.user.id, ext)
	return os.path.join("PROFESSOR-PROFILE-PIC-DIRECTORY", filename)

class ProfessorProfile(models.Model):
	user = models.OneToOneField(ProfessorAuthProfile, on_delete=models.CASCADE, related_name='ProfessorProf')
	institute = models.ForeignKey(InstituteProfile, on_delete=models.SET_NULL, blank=True, null=True)
	mobile_no = models.IntegerField(blank=True, null=True)
	gender = models.ForeignKey(GenderChoice, on_delete=models.SET_NULL, null=True, blank=True)
	date_of_birth = models.DateField(blank=False, null=False)
	address_city = models.CharField(max_length=200)
	address_district = models.CharField(max_length=200)
	address_state = models.CharField(max_length=200)
	address_country = models.CharField(max_length=200)
	address_pincode = models.IntegerField(null=True, blank=True)
	profile_pic = models.ImageField(upload_to=get_professor_profile_pic_path, null=True, blank=True, default='/PROFESSOR-PROFILE-PIC-DIRECTORY/professor_avatar.png')
	qualification = models.CharField(max_length=100, null=True, blank=True)

	email_address_verified = models.BooleanField(default=False)
	mobile_no_address_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.user.username) + ' --> ' + str(self.mobile_no)