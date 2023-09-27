from django.db import models
from .managers import UserManager
from .constants import DEFAULT_LOGIN_ATTEMPT_BUDGET
from django.contrib.auth.models import AbstractUser
from openunited.mixins import TimeStampMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser, TimeStampMixin):
    remaining_budget_for_failed_logins = models.PositiveSmallIntegerField(default=3)
    password_reset_required = models.BooleanField(default=False)
    is_test_user = models.BooleanField(_("Test User"), default=False)

    objects = UserManager()

    def reset_remaining_budget_for_failed_logins(self):
        self.remaining_budget_for_failed_logins = DEFAULT_LOGIN_ATTEMPT_BUDGET
        self.save()

    def update_failed_login_budget_and_check_reset(self):
        self.remaining_budget_for_failed_logins -= 1

        if self.remaining_budget_for_failed_logins == 0:
            self.password_reset_required = True

        self.save()

    def __str__(self):
        return f"{self.username} - {self.remaining_budget_for_failed_logins} - {self.password_reset_required}"