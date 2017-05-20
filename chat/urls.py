from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static # to remove in prod
from django.contrib import admin
from rest_framework_nested import routers

from .views import about, new_room, chat_room, MessagesViewSet, RoomsViewSet, RoomMessagesViewSet
from authentication.views import AuthRegister, AccountViewSet #AccountListView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'messages', MessagesViewSet)
router.register(r'rooms', RoomsViewSet)

rooms_router = routers.NestedSimpleRouter( #router for getting messages in room view
    router, r'rooms', lookup='room'
)
rooms_router.register(r'messages', RoomMessagesViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/auth/', include('authentication.urls')),
    url(r'^api/v1/register', AuthRegister.as_view()),
    #url(r'^api/v1/accounts', AccountListView.as_view()),
    url(r'^api/v1/', include(rooms_router.urls)),

    url(r'^$',  about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^new/$', new_room, name='new_room'),
    url(r'^room/(?P<label>[\w-]{,50})/$', chat_room, name='chat_room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)