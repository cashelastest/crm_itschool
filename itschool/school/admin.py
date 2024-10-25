from django.contrib import admin
from django.apps import apps

def auto_register_models():
    app_models = apps.get_app_config('school').get_models()
    for model in app_models:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass

auto_register_models()
# Register your models here.
