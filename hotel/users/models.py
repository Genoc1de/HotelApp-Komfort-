from django.db import models
from django.contrib.auth.models import User

class CustomUser(User):
    age = models.PositiveIntegerField(default=0)

