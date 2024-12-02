from django.contrib import admin


from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'date_of_birth',
                    'home_address', 'delivery_address', 'created', 'updated']
    list_filter = ['gender', 'created', 'updated']
    raw_id_fields = ['user']
