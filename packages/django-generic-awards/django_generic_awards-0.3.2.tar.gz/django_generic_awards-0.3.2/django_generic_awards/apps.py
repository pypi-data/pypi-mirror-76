from django.apps import AppConfig
from django.contrib import admin


class DjangoGenericAwardsConfig(AppConfig):
    EXCLUDED_ADMIN_MODULES = ('django.contrib', 'tof.models')
    name = 'django_generic_awards'

    def ready(self):
        from django_generic_awards.admin import GenericAwardsAdminMixin

        for admin_model, admin_model_object in admin.site._registry.items():
            if self.check_excluded(admin_model):
                continue

            admin_model_class = admin_model_object.__class__
            if GenericAwardsAdminMixin not in admin_model_class.__bases__:
                admin_model_class.__bases__ = (GenericAwardsAdminMixin,) + admin_model_class.__bases__
        return

    def check_excluded(self, admin_model):
        for skip_module in self.EXCLUDED_ADMIN_MODULES:
            if skip_module in admin_model.__module__:
                return True
        return False
