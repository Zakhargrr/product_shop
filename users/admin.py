from django.contrib import admin

from users.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
