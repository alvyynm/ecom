from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomRegisterForm, UserEditForm, ProfileEditForm


def register(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Signup successful. Please login.")
            return redirect('login')
        else:
            messages.error(request, "An error occurred while signing you up.")
    else:
        form = CustomRegisterForm()
    return render(request, "registration/register.html",
                  {'form': form})


@login_required
def update_user_details(request):
    """Edit user details"""
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(
            request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'authentication/user_edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
