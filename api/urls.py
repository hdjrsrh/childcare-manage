# childcare/api/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, welcome, signup, signup_educator, signup_assistant, signup_parent
from .views import user_login, user_logout, profile_view, manage_accounts, edit_accounts, delete_account
from .views import search_accounts, confirm_delete, plan_activities, mark_attendance, view_attendance
from .views import edit_profile_view, settings_view, check_site

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('check-site/', check_site, name='check_site'),
    path("welcome/", welcome, name="welcome"),
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),

    path("signup/educator/", signup_educator, name="signup_educator"),
    path("signup/assistant/", signup_assistant, name="signup_assistant"),
    path("signup/parent/", signup_parent, name="signup_parent"),    

    path("profile/", profile_view, name="profile"),
    path("manage_accounts/", manage_accounts, name="manage_accounts"),
    path("edit_accounts/<int:pk>/", edit_accounts, name="edit_accounts"),
    path("delete_account/<int:pk>/", delete_account, name="delete_account"),
    path("search_accounts/", search_accounts, name="search_accounts"),
    path("confirm_delete/", confirm_delete, name="confirm_delete"),    
    path("plan_activities/", plan_activities, name="plan_activities"),
    path("mark_attendance/", mark_attendance, name="mark_attendance"),
    path("view_attendance/", view_attendance, name="view_attendance"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
    path("settings/", settings_view, name="settings"),
]

# Ajoute les routes de l'API (DRF)
urlpatterns += router.urls
