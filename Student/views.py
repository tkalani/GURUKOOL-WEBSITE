from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse

group_name = 'Student'
login_url = 'UserAuth:landingPage'

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
		return render(request, 'Student/dashboard.html')