#from smtplib import SMTPException
import hashlib, random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.conf import settings
from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from chat.auth_classes import CsrfExemptSessionAuthentication

class AuthRegister(APIView):
    """
    Register a new user.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = AccountSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def paginate_queryset(self, queryset, view=None): # turn off pagination
        return None

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)
    
    """
    def retrieve(self, request, pk):
        context = {'request': request}
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    """
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        #print(request.data)
        if serializer.is_valid(raise_exception=True):
            Account.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'detail': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):      # deactivating instead of deleting
        acc = Account.objects.get(pk=request.user.pk)
        acc.enabled = False
        acc.save()
        #update_session_auth_hash(request, acc)  #no need because we dont use sessions here
        return Response({
            'status': 'Deactivated',
            'detail': 'User deactivated.'
        }, status=status.HTTP_204_NO_CONTENT)

"""
def forgot_password(request):
    if request.method == 'GET':
        user = Account.objects.get(username=request.GET['username'])
        new_password = hashlib.sha1(str(random.random())).hexdigest()[:8]
        subject = 'New password for {0}'.format(user.username) 
        content = 'Your new password is: {0} \nYou can change it after you  \
            login.\n\nDon\'t answer to this email. I will not read.'.format(new_password)
        print(new_password)
        try:
            send_mail(subject, content, settings.DEFAULT_FROM_EMAIL,
                      [user.email], fail_silently=False)
        except Exception:
            return HttpResponse('Can\'t send email, will not reset now.', status=500)
        user.set_password(new_password)
        user.save()
        return HttpResponse(status=204)
"""