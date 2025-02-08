# childcare/childcare/urls.py
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

# URLs that don't need language prefixes
urlpatterns = [
    path('', lambda request: redirect('/welcome/')),
    path("admin/", admin.site.urls),
    path("", include("api.urls")),  # Root URL is now outside i18n_patterns
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs that require language prefixes
urlpatterns += i18n_patterns(
    path('setlang/', set_language, name='set_language'),
)

