# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from products.models import Wishlist
from django.dispatch import receiver
from django.db.models.signals import post_save , post_delete
# Create your models here.
class CustomUsers(AbstractUser):
   user_photo = models.ImageField(upload_to='users/', blank=True, null=True)


class UserLogs(models.Model):
   userlogs_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
   userlogs_action = models.CharField(max_length=100,blank=True,null=True)
   userlogs_created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return '{0} - {1} - {2}'.format(self.userlogs_user, self.userlogs_action, self.userlogs_created)

