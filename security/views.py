from django.shortcuts import render, redirect
from .forms import SignInForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from .models import User

# Create your views here.
class SignInView(TemplateView):
    form_class = SignInForm
    initial = {}
    template_name = "security/sign_in/sign_in.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user_obj = User.objects.get_or_none(username=username)
            if user_obj:
                if user_obj.password_reset_required:
                    return redirect("password_reset_required")

            else:
                form.add_error(None, _("This username is not registered"))
                return render(request, self.template_name, {"form": form})

            user = authenticate(request, username=username, password=password)

            # TODO: create SignInAttempt for the both cases
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                user_obj.update_failed_login_budget_and_check_reset()
                form.add_error(None, _("Username or password is not correct"))

        return render(request, self.template_name, {"form": form})