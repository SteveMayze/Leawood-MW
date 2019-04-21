from django.shortcuts import render

def devices( request ):
	return render(request, 'devices/devices.html')


def pairing( request ):
	return render(request, 'devices/pairing.html')
