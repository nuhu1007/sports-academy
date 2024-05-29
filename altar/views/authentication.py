from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from altar.forms.user import LoginForm

# Create your views here.
class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request):
        form = LoginForm()

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                auth_login(request, user)
                messages.success(request, f'Successfully logged in!')
                return redirect('dashboard')
            else:
                messages.error(request, f'Invalid email or password.')
        else:
            messages.warning(request, f"{form.errors}")

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        auth_logout(request)
        messages.success(request, f"Successfully logged out!")
        return redirect('login')


class ResetPasswordView(PasswordResetView, SuccessMessageMixin):
    template_name = 'authentication/password-reset.html'
    email_template_name = 'authentication/password-reset-email.html'
    subject_template_name = 'authentication/password-reset-subject.txt'
    success_message = "We have sent you an email with instructions for changing your password." \
                      "If an account exists with the email you entered, you should receive them shortly." \
                      "If you don't receive an email, " \
                      "please make sure you entered the address you registered with and check your spam folder."
    success_url = reverse_lazy("verification")


class VerificationEmail(TemplateView):
    template_name ="authentication/verification-email-sent.html"