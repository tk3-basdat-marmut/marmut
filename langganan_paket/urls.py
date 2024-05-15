from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe_package, name='subscribe_package'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
    path('search/', search, name='search'),
    path('downloaded/', views.downloaded_songs, name='downloaded_songs'),
]