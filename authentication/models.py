from __future__ import unicode_literals
import os
import datetime
from django.core.cache import cache
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from django.conf import settings

from .utils import resize_avatar_picture

class AccountManager(BaseUserManager):
    def create(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=40, unique=True)
    username = models.CharField(max_length=20, unique=True,
      validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username.', 'invalid')
        ])
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    tagline = models.CharField(max_length=140, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='profile_pics', blank=True, 
        default="profile_pics/default_profile.jpg")
    enabled = models.BooleanField(default=True, verbose_name='Enabled')

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        pic_is_new = False
        try:
            this_record = Account.objects.get(pk=self.pk)
            if this_record.picture != self.picture:
                pic_is_new = True
                if "default_profile.jpg" not in this_record.picture.path:
                    fullpath, ext = os.path.splitext(this_record.picture.path)
                    new_name, new_name_ext = os.path.splitext(self.picture.name)
                    #print(fullpath + "_post" + ext)
                    try:
                        os.remove(fullpath + "_post" + ext)
                        os.remove(fullpath + "_comment" + ext)
                        self.picture.name = new_name + new_name_ext.lower()
                    except EnvironmentError as err:
                        print('File not found: ', fullpath, err)
                    this_record.picture.delete(save = False)
                    
        except ValueError:
            pass
        except ObjectDoesNotExist:
            pass
        super(Account, self).save(*args, **kwargs)
        if pic_is_new:
            resize_avatar_picture(self.picture)
            fullname, ext = os.path.splitext(self.picture.name)
            new_name = fullname + '.jpg'
            print('old_name: ', self.picture.name, 'new_name: ', new_name)
            if self.picture.name != new_name and "default_profile.jpg" not in self.picture.path:
                try:
                    os.remove(self.picture.path)
                except EnvironmentError as err:
                    print('File not found: ', err)
            self.picture.name = new_name
            super(Account, self).save(*args, **kwargs)   # save with right picture filename

    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def is_online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def as_dict(self):
        return {'email': self.email, 
                'username': self.username, 
                'picture': self.picture.url,
                'id': self.pk,
                'tagline': self.tagline
               }