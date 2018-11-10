from django.contrib import admin
from .models import *

admin.site.register(ProfessorProfile)
admin.site.register(CourseProfessor)
admin.site.register(Course)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(Quiz)
admin.site.register(QuizOptions)
admin.site.register(QuizQuestion)
admin.site.register(ConductQuiz)
admin.site.register(ConductPoll)
admin.site.register(QuizStatistics)