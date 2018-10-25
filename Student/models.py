from django.db import models
from django.contrib.auth.models import User
from UserAuth.models import *

from Professor.models import Course, ConductQuiz, QuizQuestion

def get_student_profile_pic_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (instance.user.id, ext)
	return os.path.join("STUDENT-PROFILE-PIC-DIRECTORY", filename)

class StudentProfile(models.Model):
	user = models.OneToOneField(StudentAuthProfile, on_delete=models.CASCADE, related_name='StudentProf')
	institute = models.ForeignKey(InstituteProfile, on_delete=models.SET_NULL, blank=True, null=True)
	mobile_no = models.CharField(max_length=1000,blank=True, null=True)
	gender = models.ForeignKey(GenderChoice, on_delete=models.SET_NULL, null=True, blank=True)
	date_of_birth = models.DateField(blank=False, null=False)
	address_city = models.CharField(max_length=200)
	address_district = models.CharField(max_length=200)
	address_state = models.CharField(max_length=200)
	address_country = models.CharField(max_length=200)
	address_pincode = models.IntegerField(null=True, blank=True)
	profile_pic = models.ImageField(upload_to=get_student_profile_pic_path, null=True, blank=True, default='/STUDENT-PROFILE-PIC-DIRECTORY/student_avatar.png')

	email_address_verified = models.BooleanField(default=False)
	mobile_no_address_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.user.username) + ' --> ' + str(self.mobile_no)

class CourseStudent(models.Model):
	student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, blank=True)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return str(self.student.user.user.username) + ' --> ' + str(self.course.name)

class QuizResults(models.Model):
	student = models.OneToOneField(StudentProfile, on_delete=models.SET_NULL, null=True, blank=True)
	conduct_quiz = models.OneToOneField(ConductQuiz, on_delete=models.SET_NULL, null=True, blank=True)
	marks_obtained = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return str(self.student.user.user.username) + '-->' +str(self.conduct_quiz.quiz.title)

class QuestionWiseResults(models.Model):
	quiz_result = models.OneToOneField(QuizResults, null=True, blank=True)
	question = models.OneToOneField(QuizQuestion, null=True, blank=True)
	marks_obtained = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return str(self.quiz_result.student.user.user.username) + '-->' +str(self.question.question)
