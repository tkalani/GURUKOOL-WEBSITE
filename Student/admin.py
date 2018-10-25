from django.contrib import admin
from .models import *

admin.site.register([StudentProfile, CourseStudent])
admin.site.register([QuizResults, QuestionWiseResults])
