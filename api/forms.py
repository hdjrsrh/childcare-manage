# childcare/api/forms.py
from .models import Account
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms  
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  
from django.core.exceptions import ValidationError
from .models import Presence
import re
from .models import CustomUser, Document, ProofOfIdentity

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'role', 'first_name', 'last_name', 'date_of_birth', 'adresse', 'diplome', 'documents', 'child_name', 'child_age', 'proof_of_identity']

    user_type = forms.ChoiceField(choices=[('child', 'Child'), ('parent', 'Parent'), ('educator', 'Educator'), ('assistant', 'Assistant')])
    date_of_birth = forms.DateField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        # Dynamically include role-specific fields based on the role
        if self.instance and self.instance.role == 'educatrice':
            self.fields['adresse'].required = True
            self.fields['diplome'].required = True
            self.fields['documents'].required = True
        elif self.instance and self.instance.role == 'parent':
            self.fields['child_name'].required = True
            self.fields['child_age'].required = True
            self.fields['proof_of_identity'].required = True
        # Add more logic for other roles as needed


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Allow multiple files

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)

# childcare/api/forms.py
class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('educatrice', 'Éducatrice'),
        ('assistante', 'Assistante'),
        ('parent', 'Parent'),
    ]

    def __init__(self, *args, role=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role

        if role == 'educatrice' or role == 'assistante':
            self.fields['adresse'] = forms.CharField(max_length=255, required=True)
            self.fields['diplome'] = forms.CharField(max_length=100, required=True)
            self.fields['documents'] = MultipleFileField(required=True)  # Use custom widget
        elif role == 'parent':
            self.fields['child_name'] = forms.CharField(max_length=100, required=True)
            self.fields['child_age'] = forms.IntegerField(required=True)
            self.fields['proof_of_identity'] = MultipleFileField(required=True)  # Use custom widget

    class Meta:
        model = CustomUser
        fields = ('username', 'nom', 'prenom', 'email', 'num_tel', 'password1', 'password2', 'role', 'adresse', 'diplome', 'documents', 'child_name', 'child_age', 'proof_of_identity')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
    
    def clean_num_tel(self):
        num_tel = self.cleaned_data.get('num_tel')
        if not re.match(r'^0\d{9}$', num_tel):
            raise ValidationError("Phone number must be 10 digits and start with 0.")
        return num_tel

    def clean_child_age(self):
        age = self.cleaned_data.get('child_age')
        if age and age >= 6:
            raise ValidationError("Child age must be under 6 years old.")
        return age


class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['user', 'date', 'present']