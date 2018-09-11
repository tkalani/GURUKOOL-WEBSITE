from django.shortcuts import render

def show_message(request):
	return render(request, 'UserAuth/message.html')