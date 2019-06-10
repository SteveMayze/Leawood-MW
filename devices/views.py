from django.shortcuts import render
from devices.models import Device
def devices( request ):

	context_dict = {}
	# context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	# context_dict["titlebar"] = "Leawood - Devices"
	# context_dict["object_list"] = queryset_l
	# context_dict["object_register"] = queryset_r
	# context_dict["page_request_var"] = page_request_var
	# context_dict["tab_request_var"] = tab_request_var
	pending_qs = Device.objects.filter(registered = False )
	active_qs = Device.objects.filter(registered = True )

	context_dict["pending_objects"] = pending_qs
	context_dict["active_objects"] = active_qs

	context_dict["current_tab"] = 'active'
	response = render(request, 'devices/devices.html', context=context_dict)
	return response

