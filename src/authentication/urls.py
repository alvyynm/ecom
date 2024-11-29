from django.urls import include, path
from . import views

# app_name = 'authentication'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('user/edit', views.update_user_details, name='update_user_details'),
]
