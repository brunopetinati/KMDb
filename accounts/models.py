from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # ao usar o AbstractUser, alterar configuração em .admin.py
    pass

