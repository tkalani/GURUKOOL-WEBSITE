from django.shortcuts import render
from Meeting.models import Meeting
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from Meeting.models import Meeting
from django.contrib import messages
# Create your views here.

def meeting_detail(request, meeting_id):
    if request.method == 'GET':
        meeting_data = Meeting.objects.get(id=meeting_id)
        if meeting_data.professor.user.user.id == request.user.id:
            return render(request, 'Meeting/meeting-detail.html', {"meeting": meeting_data})
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    if request.method == 'POST':
        try:
            status = request.POST['status']
            resp = request.POST['prof_response']

            meeting_inst = Meeting.objects.get(id=meeting_id)
            meeting_inst.status = status
            meeting_inst.prof_response = resp
            meeting_inst.save()

            messages.success(request, status+" Sccuessfully.")
            return HttpResponseRedirect(reverse('Meeting:meeting-detail', kwargs={'meeting_id': meeting_id}))
        except Exception as e:
            print(e)
            messages.warning(request, "Some Error Occurred. Please try again later")
            return HttpResponseRedirect(reverse('Professor:dashboard'))