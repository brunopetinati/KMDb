from django.contrib import admin

# ao usar AbstractUser na model, fazer as alterações a partir dessa linha
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)


# ao terminar, no settings, adicionar linha AUTH_USER_MODEL = "accounts.User" na linha 45

# Register your models here.


