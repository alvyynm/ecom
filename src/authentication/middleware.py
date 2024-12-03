from django.shortcuts import redirect
from django.urls import reverse


class OnboardingMiddleware:
    """Redirect users to onboarding if their profile is incomplete."""

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Skip for anonymous users, onboarding path, or admin path
        if (
                request.user.is_authenticated
                and not request.path.startswith(reverse('user_onboarding'))
                and not request.path.startswith('/admin/')
                and not request.path.startswith(reverse('user_account_overview'))
                and not request.path.startswith(reverse('logout'))
        ):
            if not request.user.profile.profile_complete:
                return redirect('user_onboarding')
        return self.get_response(request)
