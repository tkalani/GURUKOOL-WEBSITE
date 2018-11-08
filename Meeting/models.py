from django.db import models
from Student.models import StudentProfile
from Professor.models import ProfessorProfile


class Meeting(models.Model):
    STATUS_CHOICE = (
        ("REQUESTED", "requested"),
        ("APPROVED", "approved"),
        ("REJECTED", "rejected"),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=False, blank=False)
    body = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, default="REQUESTED")
    prof_response = models.CharField(max_length=1000, null=True, blank=True, default="")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ": " + self.status + " - " + self.student.user.user.username

class MeetingPlace(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True)
    meeting_date = models.DateField(null=True, blank=True)
    meeting_time = models.TimeField(null=True, blank=True)
    meeting_place = models.CharField(blank=True, null=True, max_length=1000)
    discussed = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return self.meeting.title + ": " + self.meeting.status + " - " + self.meeting.student.user.user.username