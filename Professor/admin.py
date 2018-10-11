from django.contrib import admin
from .models import *

admin.site.register(ProfessorProfile)
admin.site.register(CourseProfessor)
admin.site.register(Course)
admin.site.register(Poll)
admin.site.register(PollOption)