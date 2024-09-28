from django.conf import settings

class TapConfig:
    API_BASE_URL = settings.TAP_GATEWAY_BASE_URL
    API_KEY = settings.TAP_GATEWAY_SECRET_KEY
