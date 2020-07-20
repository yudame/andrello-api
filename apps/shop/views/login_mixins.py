import base64
from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.views import View

from apps.user.models import User


class ShopAccessMixin(UserPassesTestMixin):
    def dispatch(self, request, shop_slug="", *args, **kwargs):
        if not shop_slug and getattr(request.user, 'shop', None):
            return redirect('shop:dashboard_with_slug', request.user.shop.get_slug())
        elif not shop_slug:
            return HttpResponseNotFound()  # 404

        self.shop = get_object_or_404(Shop, slug=shop_slug)


class LineRichMenuLoginMixin(AccessMixin):
    """Authenticate a user via uuid of LineChannelMembership in LineRichMenu"""
    def dispatch(self, request, line_channel_id=None, *args, **kwargs):
        if not line_channel_id:
            return

        eid = request.GET.get('eid', "")

        lcm_uuid = urlsafe_base64_decode(eid).decode()
        line_channel_id, line_user_profile_id = lcm_uuid.split(':')
        if line_user_profile_id:
            user = User.objects.filter(line_user_profile_id=line_user_profile_id).first()
            if user:
                # todo: use something more temporary. maybe RemoteUserBackend ??
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        elif lcm_uuid:
            # in the case an unrecognizeable eid is provided
            # then immediately deny access
            self.handle_no_permission()


class OTPLoginMixin(AccessMixin):
    """Authenticate a user via username and OTP_code as get params."""
    def dispatch(self, request, *args, **kwargs):

        username, otp = request.GET.get('username'), request.GET.get('otp')
        if username and otp:
            user = User.objects.filter(username=username).first()
            if user and otp == user.get_otp():
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            elif not request.user.is_authenticated:
                # in the case that an invalid username and otp were provided AND the user was not already logged in
                # then we should immediately deny access and not allow other kinds of auth
                self.handle_no_permission()
        # other kinds of auth can be tested if no otp code attempted
