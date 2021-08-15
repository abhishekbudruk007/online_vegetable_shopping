
import re
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.shortcuts import redirect
from django.urls import resolve, reverse

IGNORE_PATHS = [
   re.compile(url.lstrip("/")) for url in getattr(settings, 'LOGIN_REQUIRED_IGNORE_PATHS', [])
]


class LoginRequiredMiddleware(AuthenticationMiddleware):
    def  process_view(self,request,view_func,*view_args,**view_kwargs):
        # import pdb;pdb.set_trace()
        if request.user.is_authenticated:
            return None
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(url.match(path) for url in IGNORE_PATHS):
                return redirect('{}'.format(reverse('users:login')))

