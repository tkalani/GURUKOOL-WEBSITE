from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
import UserAuth.utils as UserAuthutils
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *

group_name = 'Professor'
login_url = 'UserAuth:login'

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
        # if UserAuthutils.is_user_verfied(request):
        #     poll_list = Poll.objects.filter(professor__user__user__username=request.user.username)
        #     return render(request, 'Professor/dashboard.html', {"poll_list": poll_list})
        # else:
        #     # return render(request, 'Professor/verify_account.html')
        #     return render(request, 'Professor/dashboard.html')
        # poll_list = Poll.objects.filter(professor__user__user__username=request.user.username)
        # print(poll_list)
        # return render(request, 'Professor/dashboard.html', {"poll_list": poll_list})
        return render(request, 'Professor/dashboard.html')

@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def create_poll(request):
    if request.method == 'GET':
        course_list = CourseProfessor.objects.filter(professor__user__user__username=request.user.username)
        return render(request, 'Professor/create-poll.html', {'course_list': course_list})

    if request.method == 'POST':
        course = request.POST.get('course')
        title = request.POST.get('title')
        question = request.POST.get('question')
        option_list = request.POST.getlist('poll_options[]')

        print(option_list)

        try:
            poll_inst = Poll()
            poll_inst.professor = ProfessorProfile.objects.get(user__user__username=request.user.username)
            poll_inst.course = Course.objects.get(id=course)
            poll_inst.title = title
            poll_inst.question = question
            poll_inst.save()

            for option in option_list:
                option_inst = PollOption()
                option_inst.poll = poll_inst
                option_inst.option = option
                option_inst.save()
            return HttpResponseRedirect(reverse('Professor:dashboard'))
        except Exception as e:
            print(e)

# def show_poll(request, poll_id):
#     if request.method == 'GET':
#         poll_details = Poll.objects.get(id=poll_id)
#         poll_options = PollOption.objects.filter(poll__id=poll_id)
#         return render(request, 'Professor/poll-detail.html', {"poll_details": poll_details, 'poll_options': poll_options})