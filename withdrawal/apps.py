from django.apps import AppConfig


class WithdrawalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'withdrawal'
    def ready(self):
        import withdrawal.signal
