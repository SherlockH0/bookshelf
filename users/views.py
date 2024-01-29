from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import views

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(
                request, 'Account created successfuly! You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(
                request, 'Your account has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {'form': form}

    return render(request, 'users/profile.html', context)


class CustomLoginView(views.LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(
            self.request, f'You have been successfuly logged in!')
        return super().form_valid(form)


class CustomLogoutView(views.LogoutView):
    template_name = 'users/logout.html'
