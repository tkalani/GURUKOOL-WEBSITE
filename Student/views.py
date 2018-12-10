from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from .models import *
from Doubt.models import *
from Meeting.models import *
from Professor.models import *

group_name = 'Student'
login_url = 'UserAuth:landingPage'

def group_required(*group_names, login_url=None):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def dashboard(request):
	if request.method == 'GET':
		return render(request, 'Student/dashboard.html')

@login_required(login_url=login_url)
def profile(request, student_id):
    try:
        results = QuizResult.objects.filter(student__user__user__id=student_id,conduct_quiz__quiz__professor__can_view=True).order_by('-conduct_quiz__conduction_date')
        student_profile = StudentProfile.objects.get(user__user__id=student_id)
        courses = CourseStudent.objects.filter(student__user__user__id=student_id)

        meetings = MeetingPlace.objects.filter(meeting__student__user__user__id=student_id)

        course_list = CourseProfessor.objects.filter(professor__user__user__id=request.user.id).order_by('-id')
        all_doubt_list = []
        for course in course_list:
                for y in Doubt.objects.filter(course__id=course.course.id, student__user__user__id=student_id):
                        all_doubt_list.append(y)
        all_doubt_list = sorted(all_doubt_list, key=lambda k: k.last_updated)
        all_doubt_list = all_doubt_list[::-1]
        
        return render(request, 'Student/profile.html', {"meetings": meetings, "doubts": all_doubt_list, "results": results, "student_profile": student_profile, "courses": courses})
    except Exception as e:
        print(e)
        return HttpResponse("This student doesn't exist")