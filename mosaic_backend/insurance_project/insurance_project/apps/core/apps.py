from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insurance_project.apps.core'
    label = 'core'
    verbose_name = 'Core'


