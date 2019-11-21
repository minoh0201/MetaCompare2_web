from django.shortcuts import render

# Create your views here.

# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User

class UserCreationForm_email(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class SignUp(generic.CreateView):
    form_class = UserCreationForm_email
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was Changed successfully!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error(s) mentioned below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})