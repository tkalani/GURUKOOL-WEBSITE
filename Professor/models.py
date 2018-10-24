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
	mobile_no = models.CharField(max_length=1000,blank=True, null=True)
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

class Course(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)
	code = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return str(self.name) + ' --> ' + str(self.code)

class CourseProfessor(models.Model):
	professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return str(self.professor.user.user.username) + ' --> ' + str(self.course.name)

class Poll(models.Model):
	professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=100, null=False, blank=False)
	question = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return str(self.professor.user.user.username) + ' --> ' + str(self.course.name)+ ' --> ' + str(self.title)

class PollOption(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	option = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return str(self.poll.id) + ' --> ' + str(self.option)

class Quiz(models.Model):
	professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=100, null=False, blank=False)
	description = models.TextField(null=True, blank=True)
	pass_marks = models.IntegerField(default=0)
	max_marks = models.IntegerField(default=0)
	no_of_questions = models.IntegerField(default=0)

	def __str__(self):
		return str(self.professor) + ' --> ' + str(self.course) + ' --> ' + str(self.title)

class QuizQuestion(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
	question = models.CharField(max_length=100, null=False, blank=False)
	question_file = models.ImageField(null=True, blank=True)
	marks = models.IntegerField(default=0)
	time = models.IntegerField(default=0)

	def __str__(self):
		return str(self.quiz.id) + ' --> ' + str(self.id)

class QuizOptions(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
	question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True, blank=True)
	option = models.TextField(null=False, blank=False)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return str(self.option) + ' --> ' + str(self.quiz.id) + ' --> ' + str(self.question.id) + ' --> ' + str(self.is_correct)

class ConductQuiz(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False, blank=False)
	unique_quiz_id = models.CharField(max_length=100, null=False, blank=False)
	active = models.BooleanField(default=False)
	conduction_date = models.DateField(default=False)
	conduction_time = models.BooleanField(default=False)

	def __str__(self):
		return str(self.quiz) + '-->' + str(self.unique_quiz_id)