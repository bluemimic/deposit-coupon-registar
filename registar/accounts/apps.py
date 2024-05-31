from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.core.signals import request_finished


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = _('accounts')
    
    def ready(self):
        import accounts.signals
