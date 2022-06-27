from django.apps import AppConfig


class MainlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainList'
    verbose_name = 'Соревнования'

    def ready(self):
        import mainList.signals