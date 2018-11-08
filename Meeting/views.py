from django.shortcuts import render
from Meeting.models import Meeting
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from Meeting.models import *
from django.contrib import messages
# Create your views here.

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