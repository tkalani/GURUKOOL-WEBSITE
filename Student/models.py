from django.db import models
from django.contrib.auth.models import User
from UserAuth.models import *

def get_student_profile_pic_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (instance.user.id, ext)
	return os.path.join("STUDENT-PROFILE-PIC-DIRECTORY", filename)

class StudentProfile(models.Model):
	user = models.OneToOneField(StudentAuthProfile, on_delete=models.CASCADE, related_name='StudentProf')
	institute = models.ForeignKey(InstituteProfile, on_delete=models.SET_NULL, blank=True, null=True)
	mobile_no = models.IntegerField(blank=True, null=True)
	gender = models.ForeignKey(GenderChoice, on_delete=models.SET_NULL, null=True, blank=True)
	date_of_birth = models.DateField(blank=False, null=False)
	salary = models.IntegerField(blank=True, null=True)
	address_city = models.CharField(max_length=200)
	address_district = models.CharField(max_length=200)
	address_state = models.CharField(max_length=200)
	address_country = models.CharField(max_length=200)
	address_pincode = models.IntegerField(null=True, blank=True)
	profile_pic = models.ImageField(upload_to=get_student_profile_pic_path, null=True, blank=True, default='/PROFESSOR-PROFILE-PIC-DIRECTORY/professor_avatar.png')

	email_address_verified = models.BooleanField(default=False)
	mobile_no_address_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.user.username) + ' --> ' + str(self.mobile_no)