from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.package_list, name='packages'),
    path('payment/<int:package_id>/', views.payment, name='payment'),
    path('history/', views.transaction_history, name='history'),
]