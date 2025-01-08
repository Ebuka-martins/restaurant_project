from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'

    # This imports and registers the signals
    def ready(self):
        import booking.signals 
