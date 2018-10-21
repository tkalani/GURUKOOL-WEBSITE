from django.shortcuts import render
from Meeting.models import Meeting
from django.http import HttpResponseNotFound
from Meeting.models import Meeting
# Create your views here.

def meeting_detail(request, meeting_id):

    if request.method == 'GET':
        meeting_data = Meeting.objects.get(id=meeting_id)
        if meeting_data.professor.user.user.id == request.user.id:
            return render(request, 'Meeting/meeting-detail.html', {"meeting": meeting_data})
        return HttpResponseNotFound('<h1>Page not found</h1>')
