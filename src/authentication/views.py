from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomRegisterForm, UserEditForm, ProfileEditForm
from .models import Profile


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

            # mark profile as completed
            user_profile = request.user.profile
            user_profile.profile_complete = True
            user_profile.save()
            messages.success(request, "Profile complete. Happy shopping!")

            return redirect('user_account_overview')
        else:
            messages.error(
                request, "There's an issue with your profile details, fix and try again.")

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'authentication/user_edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_account_overview(request):
    """Displays the user's account details"""
    user_data = request.user
    profile_data = user_data.profile
    orders = user_data.orders.all()
    return render(request, 'authentication/user_account_overview.html',
                  {
                      'user_data': user_data,
                      'profile_data': profile_data,
                      'orders': orders
                  })


def user_onboarding(request):
    """Onboarding page to allow the user to add more details to the profile"""
    if request.method == 'POST':
        profile_form = ProfileEditForm(
            request.POST, instance=request.user.profile)
        user_profile = request.user.profile
        if profile_form.is_valid():
            profile_form.save()
            user_profile.profile_complete = True
            user_profile.save()
            messages.success(request, "Profile complete. Happy shopping!")
            return redirect('shop:product_list')
        else:
            messages.error(
                request, "There's an issue with your profile details, fix and try again.")

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'authentication/onboarding.html',
                  {'profile_form': profile_form})
