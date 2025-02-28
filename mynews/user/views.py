from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                if 'profile_picture' in request.FILES:
                    profile_pic = request.FILES['profile_picture']
                    file_path = default_storage.save(f"profile_pics/{profile_pic.name}", profile_pic)
                    user.profile_picture = file_path

                user.save()
                login(request, user)
                return redirect('post_list')
            except Exception as e:
                logger.exception("An error occurred during registration:")  # Log the exception with traceback
                form.add_error(None, "An error occurred during registration. Please try again.") # User-friendly message
                # Consider a more generic message for production:
                # form.add_error(None, "An error occurred. Please try again later.")

        else:
            # Log form errors, but don't expose details to the user in production
            logger.warning("Invalid registration form: %s", form.errors.as_json()) #Log the errors
            form.add_error(None, "Invalid registration data. Please check the form.") # Generic message

    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list') # Redirect to post list or a user's profile page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('post_list') 

@login_required
def view_profile(request):
    user = request.user  # Get the logged-in user
    return render(request, 'users/profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user) # Add request.FILES for image upload
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})