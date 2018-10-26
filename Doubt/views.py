from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import *
from Professor.models import Course

student_group = 'Student'
prof_group = 'Professor'
login_url = 'UserAuth:login'

def group_required(*group_names, login_url=None):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)


@login_required(login_url=login_url)
@group_required(prof_group, login_url=login_url)
def show_doubt(request, course_id):
    if request.method == 'GET':
        doubts = Doubt.objects.filter(course__id=course_id)
        course = Course.objects.get(id=course_id)
        # print(doubts)
        return render(request, 'Doubt/doubt.html', {"doubt_list": doubts, "course":course})

@login_required(login_url=login_url)
def create_comment(request, doubt_id):
    if request.method == 'POST':
        text = request.POST['comment']
        doubt = Doubt.objects.get(id=doubt_id)
        comment = Comment.objects.create(doubt=doubt, user_id=request.user.id, text=text)
        # return HttpResponseRedirect(reverse('Doubt:doubt-list',kwargs={'course_id':doubt.course.id}))
        return HttpResponseRedirect(reverse('Doubt:doubt', kwargs={'doubt_id': doubt_id}))

@login_required(login_url=login_url)
@group_required(prof_group, login_url=login_url)
def doubt(request, doubt_id):
        if request.method == 'GET':
                try:
                        doubt = Doubt.objects.get(id=doubt_id)
                        return render(request, 'Doubt/doubt-details.html', {"doubt_data": doubt})
                except Exception as e:
                        print(e)
                        messages.success(request, "Some Error Occurred")
                        return HttpResponseRedirect(reverse('Professor:dasboard'))