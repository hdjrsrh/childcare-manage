# childcare/api/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser

# Enregistre CustomUser dans l'admin
admin.site.register(CustomUser)

# Create groups if they don't exist
roles = ["admin", "directrice", "assistante_pedagogique", "educatrice", "parent"]
for role in roles:
    Group.objects.get_or_create(name=role)

