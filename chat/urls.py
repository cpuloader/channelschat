from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static # to remove in prod

from . import views

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]