from django.conf.urls import include, url
from devices import views as devices

urlpatterns = [
    url(r'^$', devices.devices, name='devices'),
]
