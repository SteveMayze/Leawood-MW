from django.db import models

class Token(models.Model):
	username = models.CharField(max_length=50, unique=True)
	uid = models.CharField(max_length=255, unique=True)

	def __str__( self ):
		return f'{self.username}-{self.uid}'