# subapp_name/urls.py
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter






urlpatterns = [
    path('ask', views.ask, name='ask'),
    path('update_order_status/', views.UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('payment', views.PlaceEventOrderAPIView.as_view(), name='place_event_order'),
    path('blog', views.BlogViewSet.as_view(), name='get-blogs'),
]
