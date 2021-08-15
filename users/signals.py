from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in,user_logged_out
from .models import UserLogs
from products.models import Wishlist
from django.db.models.signals import post_delete,post_save
@receiver(user_logged_in)
def user_logged_in_signal(sender,request,user,**kwargs):
    print("User is Logged In")
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=user,
        userlogs_action='user_logged_in',
    )


@receiver(user_logged_out)
def user_logged_out_signal(sender,request,user,**kwargs):
    print("User is Logged Out")
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=user,
        userlogs_action='user_logged_out',
    )

@receiver(post_save,sender=Wishlist)
def save_user_logs(sender,**kwargs):
    # import pdb;pdb.set_trace()
    print("sender",sender) #<class 'products.models.Wishlist'>
    instance = kwargs["instance"] #<Wishlist: Potatoes>
    print("sender",sender.wishlist_user)
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=instance.wishlist_user,
        userlogs_action='wishlist_item_added'
    )

@receiver(post_delete,sender=Wishlist)
def save_user_logs(sender,**kwargs):
    # import pdb;pdb.set_trace()
    print("sender",sender) #<class 'products.models.Wishlist'>
    instance = kwargs["instance"] #<Wishlist: Potatoes>
    print("sender",sender.wishlist_user)
    userlogs_object, created = UserLogs.objects.get_or_create(
        userlogs_user=instance.wishlist_user,
        userlogs_action='wishlist_item_deleted'
    )
