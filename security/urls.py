from django.urls import path
from .views import (
    SignInView,
)

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign_in"),
    # path("sign-up/", SignInView.as_view(), name="sign_in"),
]

urlpatterns += [
    path(
        "password-reset/",
        SignInView.as_view(),
        name="password_reset",
    ),
]