from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth import views

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(
                request, f'Account created successfully! You now can login!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class CustomLoginView(views.LoginView):
    template_name='users/login.html'

    def form_valid(self, form):
        messages.success(
                self.request, f'You have been successfully logged in!')
        return super().form_valid(form)

class CustomLogoutView(views.LogoutView):
    template_name='users/logout.html'

