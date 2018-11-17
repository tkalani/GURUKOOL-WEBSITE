from django.shortcuts import render
from Meeting.models import Meeting
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from Meeting.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

group_name = 'Professor'
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


@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def meeting_detail(request, meeting_id):
    '''
    Get the meeting details
    Takes input request method and meeting_id
    If GET request, the render the web page and if POST requets then return HHTP response
    '''
    if request.method == 'GET':
        meeting_data = Meeting.objects.get(id=meeting_id)
        meeting_place = MeetingPlace.objects.filter(meeting__id=meeting_id)
        return render(request, 'Meeting/meeting-detail.html', {"meeting": meeting_data, "meeting_detail": meeting_place})

    if request.method == 'POST':
        try:
            status = request.POST['status']
            resp = request.POST['prof_response']

            meeting_inst = Meeting.objects.get(id=meeting_id)
            meeting_inst.status = status
            meeting_inst.prof_response = resp
            meeting_inst.save()

            inst = MeetingPlace()
            inst.meeting = meeting_inst
            inst.meeting_date = request.POST.get('meeting_date')
            inst.meeting_time = request.POST.get('meeting_time')
            inst.meeting_place = request.POST.get('meeting_place')
            inst.save()

            messages.success(request, status+" Sccuessfully.")
            return HttpResponseRedirect(reverse('Meeting:meeting-detail', kwargs={'meeting_id': meeting_id}))
        except Exception as e:
            print(e)
            messages.warning(request, "Some Error Occurred. Please try again later")
            return HttpResponseRedirect(reverse('Professor:dashboard'))


@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def index(request):
    meeting_list = Meeting.objects.filter(professor__user__user__id=request.user.id).order_by('-created_time')
    return render(request, 'Meeting/all-meetings.html', {'all_meeting_list': meeting_list})


@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def meeting_happened(request, meeting_id):
    print("meeting ", meeting_id)
    if request.method == 'POST':
        try:
            discussed = request.POST['discussed']
            print("Discussion = ", discussed)
            meeting_inst = MeetingPlace.objects.get(meeting__id=meeting_id)
            meeting_inst.discussed = discussed
            meeting_inst.is_happened = True
            meeting_inst.is_ticked = True
            meeting_inst.save()
            print(meeting_inst)
            return HttpResponseRedirect(reverse('Professor:dashboard'))
        except Exception as e:
            print(e)
            messages.warning(request, "Some Error Occurred. Please try again later")
            return HttpResponseRedirect(reverse('Professor:dashboard'))


@login_required(login_url=login_url)
@group_required(group_name, login_url=login_url)
def meeting_not_happened(request, meeting_id):
    print("meeting ", meeting_id)
    if request.method == 'POST':
        try:
            discussed = request.POST['discussed']
            print("Discussion = ", discussed)
            meeting_inst = MeetingPlace.objects.get(meeting__id=meeting_id)
            meeting_inst.discussed = discussed
            meeting_inst.is_happened = False
            meeting_inst.is_ticked = True
            meeting_inst.save()
            print(meeting_inst)
            return HttpResponseRedirect(reverse('Professor:dashboard'))
        except Exception as e:
            print(e)
            messages.warning(request, "Some Error Occurred. Please try again later")
            return HttpResponseRedirect(reverse('Professor:dashboard'))
