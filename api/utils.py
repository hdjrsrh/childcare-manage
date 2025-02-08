# childcareapp/utils.py
from django.apps import apps

def get_current_site():
    if apps.ready:
        from django.contrib.sites.models import Site
        return Site.objects.get_current()
    return None
