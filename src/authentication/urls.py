from django.urls import include, path
from . import views

# app_name = 'authentication'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('user/edit', views.update_user_details, name='update_user_details'),
    path('user/', views.user_account_overview, name='user_account_overview'),
    path('user/onboarding', views.user_onboarding, name='user_onboarding'),
]
