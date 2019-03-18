from django.conf.urls import url
from accounts import views

urlpatterns = [
	url(r'^register$', views.register, name='accounts_register'),
	url(r'^login$', views.login, name='accounts_login'),
	url(r'^logout$', views.logout, name='accounts_logout'),
	url(r'^reset_password$', views.reset_password, name='accounts_reset_password'),
]