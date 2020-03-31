from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class food_cloudConfig(AppConfig):
    name = 'food_cloud'

    def ready(self):
        import food_cloud.signals
