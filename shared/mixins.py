from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic.base import ContextMixin


User = get_user_model()


class BaseViewMixin(ContextMixin):
    """
    Base view for all views.
    """
    page_name = None

    def get_context_data(self, **kwargs):
        kwargs.update(page_name=self.page_name)
        kwargs.update({
            'page_name': self.page_name,
            'environment': settings.ENVIRONMENT
        })
        return super().get_context_data(**kwargs)


class BaseAccessMixin(LoginRequiredMixin, UserPassesTestMixin, BaseViewMixin):
    """
    Base view to filter active users.
    """
    access_roles = []

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True

        if user.status != User.ACTIVE or user.role is None:
            return False

        elif (self.access_roles == '__all__' or
                user.role.name in self.access_roles or user.is_superuser):
            return True

    def get_permission_denied_message(self):
        user = self.request.user
        if user.status == User.PENDING:
            return 'Your account is not activated yet.'
        elif user.status == User.DISABLED:
            return 'Your account has been disabled.'
        else:
            return "You don't have the right permission to access this page."


class BaseSettingsMixin(BaseAccessMixin):
    """
    Base view for all settings pages.
    """
    page_name = 'settings'
    setting_name = None

    def get_context_data(self, **kwargs):
        kwargs.update(setting_name=self.setting_name)
        return super().get_context_data(**kwargs)
