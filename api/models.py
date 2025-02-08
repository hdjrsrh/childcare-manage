# childcare/api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class MyModel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class ProofOfIdentity(models.Model):
    file = models.FileField(upload_to='proof_of_identity/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('directrice', 'Directrice'),
        ('educatrice', 'Éducatrice'),
        ('assistante', 'Assistante'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    nom = models.CharField(max_length=30, null=True)
    prenom = models.CharField(max_length=30, null=True)
    email = models.EmailField(unique=True, null=True)
    num_tel = models.CharField(max_length=15, null=True)
    nom_institution = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    diplome = models.CharField(max_length=100, blank=True, null=True)
    documents = models.ManyToManyField(Document, blank=True)    
    child_name = models.CharField(max_length=100, blank=True, null=True)
    child_age = models.IntegerField(blank=True, null=True)
    proof_of_identity = models.ManyToManyField(ProofOfIdentity, blank=True)
    
    groups = models.ManyToManyField(
        "auth.group",
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.permission",
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.email
    
    def __str__(self):
        return f"{self.username} ({self.role})"




class Account(models.Model):
    USER_TYPE_CHOICES = [
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('educator', 'Educator'),
        ('assistant', 'Assistant'),
    ]
    
    username = models.CharField(max_length=100)
    email = models.EmailField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    diplome = models.CharField(max_length=255, blank=True, null=True)
    documents = models.FileField(upload_to='documents/', blank=True, null=True)
    child_name = models.CharField(max_length=100, blank=True, null=True)
    child_age = models.IntegerField(blank=True, null=True)
    proof_of_identity = models.FileField(upload_to='proof_of_identity/', blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username



class Presence(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'date')