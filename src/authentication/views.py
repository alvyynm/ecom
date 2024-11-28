from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomRegisterForm


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
