"""Leawood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
from django.conf.urls import include, url
from dashboard import views as home
from devices import urls as devices_urls
from accounts import urls as accounts_urls

urlpatterns = [
	url(r'^$', home.dashboard, name='dashboard'),
    url(r'^leawood/$', home.dashboard, name='dashboard'),
    url(r'^devices/', include(devices_urls)),
    url(r'^accounts/', include(accounts_urls)),
    # path('admin/', admin.site.urls),
]
