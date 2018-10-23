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
