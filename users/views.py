from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegisterForm, UserUpdateForm, CustomAuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
        else:
            print(form.errors)  # Debug form errors
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
            
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

def logout_success(request):
    return render(request, 'users/logout.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        # Store user reference before saving
        user = form.user
        response = super().form_valid(form)
        
        # Update session to prevent immediate logout
        update_session_auth_hash(self.request, user)

        # success message
        messages.success(self.request, f"Password successfuly reset! Welcome back, {user.username}!")
        
        # Debugging output
        print(f"Password changed for: {user.username}")
        print(f"New password works: {user.check_password(form.cleaned_data['new_password1'])}")
    
        return response
    
   