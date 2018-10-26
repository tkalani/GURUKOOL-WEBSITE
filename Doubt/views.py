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
    ''' checks group requirement whwther the user is student or professor
        Takes group name as input and login url
        returns status if user passes or not'''
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url=login_url)

''' login required'''
@login_required(login_url=login_url)
@group_required(prof_group, login_url=login_url)
def show_doubt(request, course_id):
    '''
        Shows all Doubts
        Takes input course_id,request
        Returns doubt_list,course and renders the web page
    '''
    if request.method == 'GET':
        doubts = Doubt.objects.filter(course__id=course_id)
        course = Course.objects.get(id=course_id)
        return render(request, 'Doubt/doubt.html', {"doubt_list": doubts, "course":course})

@login_required(login_url=login_url)
def create_comment(request, doubt_id):
    '''
       Creates a new comment
       Takes input request method and doubt_id
       returns http response if comment created successfuly 
    '''
    if request.method == 'POST':
        text = request.POST['comment']
        doubt = Doubt.objects.get(id=doubt_id)
        comment = Comment.objects.create(doubt=doubt, user_id=request.user.id, text=text)
        # return HttpResponseRedirect(reverse('Doubt:doubt-list',kwargs={'course_id':doubt.course.id}))
        return HttpResponseRedirect(reverse('Doubt:doubt', kwargs={'doubt_id': doubt_id}))

'''
Get a particular doubt
Takes input request method and doubt_id
Returns doubt_data,previous_replies and renders the web page
'''
@login_required(login_url=login_url)
@group_required(prof_group, login_url=login_url)
def doubt(request, doubt_id):
        if request.method == 'GET':
                try:
                        doubt = Doubt.objects.get(id=doubt_id)
                        previous_replies = Comment.objects.filter(doubt__id=doubt_id).order_by('-last_updated')
                        return render(request, 'Doubt/doubt-details.html', {"doubt_data": doubt, "previous_replies": previous_replies})
                except Exception as e:
                        print(e)
                        messages.success(request, "Some Error Occurred")
                        return HttpResponseRedirect(reverse('Professor:dashboard'))
