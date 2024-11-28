from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Signup successful. Please login.")
            return redirect('authentication:login')
        else:
            messages.error(request, "An error occurred while signing you up.")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html",
                  {'form': form})
