from django.urls import include, path

app_name = 'authentication'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
