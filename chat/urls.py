from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static # to remove in prod
from rest_framework_nested import routers

from .views import about, new_room, chat_room, MessagesViewSet

router = routers.SimpleRouter()
router.register(r'messages', MessagesViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),

    url(r'^$',  about, name='about'),
    url(r'^new/$', new_room, name='new_room'),
    url(r'^room/(?P<label>[\w-]{,50})/$', chat_room, name='chat_room'),
]