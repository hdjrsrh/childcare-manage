# childcare/api/views.py
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import JsonResponse
from .models import CustomUser, Presence, Account, Presence, Document, ProofOfIdentity
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AccountForm, PresenceForm, SignUpForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.core.paginator import Paginator
from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer
from rest_framework import filters



def welcome(request):
    return render(request, "welcome.html")



def signup(request):
    return render(request, 'signup.html')

def signup_educator(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES, role='educatrice')
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'educatrice'
            user.save()

            # Handle multiple file uploads for documents
            for file in request.FILES.getlist('documents'):
                document = Document.objects.create(file=file)
                user.documents.add(document)

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm(role='educatrice')

    return render(request, 'signup_role.html', {'form': form, 'role': 'educatrice'})

def signup_assistant(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES, role='assistante')  # Pass role correctly
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'assistante'
            user.save()

            # Handle multiple file uploads for documents
            for file in request.FILES.getlist('documents'):
                document = Document.objects.create(file=file)
                user.documents.add(document)

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm(role='assistante')

    return render(request, 'signup_role.html', {'form': form, 'role': 'assistante'})


def signup_parent(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES, role='parent')
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'parent'
            user.save()

            # Handle multiple file uploads for proof_of_identity
            for file in request.FILES.getlist('proof_of_identity'):
                proof = ProofOfIdentity.objects.create(file=file)
                user.proof_of_identity.add(proof)

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm(role='parent')

    return render(request, 'signup_role.html', {'form': form, 'role': 'parent'})



@login_required
def profile_view(request):
    is_admin = request.user.groups.filter(name='admin').exists()
    is_educatrice = request.user.groups.filter(name='educatrice').exists()
    is_assistante_pedagogique = request.user.groups.filter(name='assistante_pedagogique').exists()
    is_directrice = request.user.groups.filter(name='directrice').exists()
    is_parent = request.user.groups.filter(name='parent').exists()

    return render(request, 'profile.html', {
        'is_admin': is_admin,
        'is_educatrice': is_educatrice,
        'is_assistante_pedagogique': is_assistante_pedagogique,
        'is_directrice': is_directrice,
        'is_parent': is_parent,
    })



def user_login(request):  # ✅ Évite le conflit de nom
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ Utilise Django login()
            return redirect("profile")  # Redirige après connexion
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")  # Formulaire de connexion si GET


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")



def plan_activities(request):
    # Logic for creating a menu
    return render(request, 'plan_activities.html')

def confirm_delete(request):
    # Logic for creating a menu
    return render(request, 'confirm_delete.html')

# Gestion des Comptes - Add/Modify Account
@login_required
def manage_accounts(request):
    accounts_list = Account.objects.all()
    paginator = Paginator(accounts_list, 10)  # Show 10 accounts per page
    page_number = request.GET.get('page')
    accounts = paginator.get_page(page_number)

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_accounts')
    else:
        form = AccountForm()
    return render(request, 'manage_accounts.html', {'form': form, 'accounts': accounts})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['role', 'username', 'email']


# Recherche des Comptes - Search Accounts
@login_required
def search_accounts(request):
    query = request.GET.get('q', '')
    if query:
        accounts = Account.objects.filter(username__icontains=query)
    else:
        accounts = Account.objects.all()
    return render(request, 'search_accounts.html', {'accounts': accounts, 'query': query})


# Edit Account
@login_required
def edit_accounts(request, pk):
    if not request.user.groups.filter(name='directrice').exists():
        messages.error(request, "You don't have permission to edit accounts.")
        return redirect('home')  # Redirect unauthorized users
    
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('manage_accounts')  # Redirect after saving
    else:
        form = AccountForm(instance=account)
    
    return render(request, 'edit_accounts.html', {'form': form})

# Delete Account
@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('search_accounts')  # Redirect after deleting
    return render(request, 'confirm_delete.html', {'account': account})


@login_required
def mark_attendance(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        date = request.POST.get('date')
        present = request.POST.get('present') == 'true'

        user = CustomUser.objects.get(id=user_id)
        presence, created = Presence.objects.get_or_create(user=user, date=date)
        presence.present = present
        presence.save()

        return JsonResponse({'status': 'success'})
    
    users = CustomUser.objects.filter(groups__name__in=['educatrice', 'assistante_pedagogique'])
    return render(request, 'mark_attendance.html', {'users': users})


@login_required
def view_attendance(request):
    if not request.user.groups.filter(name='directrice').exists():
        messages.error(request, "You don't have permission to view attendance.")
        return redirect('home')
    
    # Fetch all attendance records
    records = Presence.objects.all().order_by('-date')
    return render(request, 'view_attendance.html', {'records': records})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Mettre à jour les informations de l'utilisateur
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')  # Redirige vers la vue du profil après la mise à jour

    return render(request, 'edit_profile.html')

def settings_view(request):
    return render(request, 'settings.html')


def create_menu(request):
    return JsonResponse({"message": "This is the create_menu endpoint"})


import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Définition des types et tailles autorisés
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Mo

@login_required
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Vérifier le type de fichier
        if file_extension not in ALLOWED_EXTENSIONS:
            return JsonResponse({"error": "Type de fichier non autorisé."}, status=400)

        # Vérifier la taille du fichier
        if uploaded_file.size > MAX_FILE_SIZE:
            return JsonResponse({"error": "Fichier trop volumineux (max 5 Mo)."}, status=400)

        # Vérifier que l'utilisateur peut modifier son propre document
        if request.user.id != request.POST.get("user_id"):  # user_id doit être envoyé avec la requête
            return JsonResponse({"error": "Vous ne pouvez modifier que vos propres fichiers."}, status=403)

        # Sauvegarde du fichier
        file_path = f"uploads/{request.user.id}/{uploaded_file.name}"
        path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        
        return JsonResponse({"message": "Fichier téléversé avec succès.", "file_path": path})

    return JsonResponse({"error": "Requête invalide."}, status=400)

from django.contrib.sites.models import Site
from django.http import HttpResponse

def check_site(request):
    current_site = Site.objects.get_current()
    return HttpResponse(f"Current site: {current_site.domain}")