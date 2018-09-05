from django.contrib import admin
from .models import *

admin.site.register(GenderChoice)
admin.site.register(InstituteProfile)
admin.site.register(ProfessorAuthProfile)
admin.site.register(StudentAuthProfile)