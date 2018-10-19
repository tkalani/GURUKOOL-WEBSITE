from django.shortcuts import render
from .models import Doubt

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
# def get_doubt(request):
#     if request.method == 'GET':