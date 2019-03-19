from django.db import models

class Token(models.Model):
	username = models.CharField(max_length=50)
	uid = models.CharField(max_length=255)
