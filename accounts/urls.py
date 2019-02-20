from django.conf.urls import url
from accounts import views

urlpatterns = [
	url(r'^register$', views.register, name='account_register'),
	url(r'^login$', views.login, name='account_login'),
]