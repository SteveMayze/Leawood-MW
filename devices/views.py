from django.shortcuts import render

def devices( request ):
	return render(request, 'devices/devices.html')