import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

def get_user_jwt(request):
    user = get_user(request)
    #print('get_user_jwt: ', user)
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            return user_jwt[0]
        else:
            return user or AnonymousUser()
    except:
        pass


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
        current_user = request.user
        if hasattr(current_user, 'username'):
            now = datetime.datetime.now()
            cache.set('seen_%s' % (current_user.username), now,
                           settings.USER_LASTSEEN_TIMEOUT)
            #print(cache.get('seen_%s' % current_user.username), current_user.username)