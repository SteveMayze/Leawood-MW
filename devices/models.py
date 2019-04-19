from django.db import models


class Location ( models.Model ):
	name = models.CharField(max_length=50, unique=True)
	longitude = models.DecimalField(max_digits=22, decimal_places=16)
	latitude = models.DecimalField(max_digits=22, decimal_places=16)
	altitude = models.DecimalField(max_digits=22, decimal_places=16)

class Device ( models.Model ):
	name = models.CharField(max_length=50, unique=True)
	serial_id = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=500)
	address = models.CharField(max_length=50, unique=True)
	registered = models.BooleanField(default=False)
	location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)


class Log_Entry( models.Model ):
	time_stamp = models.DateTimeField(auto_now_add=True)
	log_data = models.TextField(blank=True)
	device = models.ForeignKey(Device, on_delete=models.CASCADE)