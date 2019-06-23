from django.shortcuts import render
from devices.models import Device
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def devices( request ):

	context_dict = {}

	page_number_var = 'p'
	page_filter_var = 'q'
	page_tab_var = 't'

	query = request.GET.get( page_filter_var )
	current_tab = request.GET.get("t")
	if current_tab == None:
		current_tab = 'active'


	queryset_list = Device.objects.filter(registered = True ).order_by('id')
	if query and current_tab == "active":
		queryset_list = queryset_list.filter(
				Q(name__icontains=query) | 
				Q(description__icontains=query)
			).distinct()


	queryset_register = Device.objects.filter(registered = False ).order_by('id')
	if query and current_tab == "register":
		queryset_register = queryset_register.filter(
				Q(name__icontains=query) | 
				Q(description__icontains=query)
			).distinct()

	paginator_list = Paginator(queryset_list, 5)
	paginator_register = Paginator(queryset_register, 5)
	page = request.GET.get(page_number_var)
	try:
		active_qs = paginator_list.page(page)
	except PageNotAnInteger:
		active_qs = paginator_list.page(1)
	except EmptyPage:
		active_qs = paginator_list.page(paginator_list.num_pages)
	try:
		pending_qs = paginator_register.page(page)
	except PageNotAnInteger:
		pending_qs = paginator_register.page(1)
	except EmptyPage:
		pending_qs = paginator_register.page(paginator_register.num_pages)


	# context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	# context_dict["titlebar"] = "Leawood - Devices"
	context_dict["page_number_var"] = page_number_var
	context_dict["page_tab_var"] = page_tab_var
	context_dict["pending_objects"] = pending_qs
	context_dict["active_objects"] = active_qs
	context_dict["page_filter_var"] = page_filter_var

	context_dict["current_tab"] = current_tab
	response = render(request, 'devices/devices.html', context=context_dict)
	return response

