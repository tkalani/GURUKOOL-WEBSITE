from django.db import models

from Student.models import StudentProfile
from Professor.models import Course


class Doubt(models.Model):
	student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=100, null=False, blank=False)
	description = models.CharField(max_length=1000, null=False, blank=False)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "{}: {}".format(self.course.name, self.title)
