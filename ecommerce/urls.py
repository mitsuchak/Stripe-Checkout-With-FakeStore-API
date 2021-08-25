"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products import  views
from products.views import create_stripe_checkout_session,stripe_webhook
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.json_list),
    path('create_stripe_checkout_session/<str:product_name>', views.create_stripe_checkout_session, name='create_stripe_checkout_session'),
    path('success_payment.html', views.success_payment.as_view(), name='success_payment'),
    path('cancel_payment.html', views.cancel_payment.as_view(), name='success_payment'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('order.html', views.order, name='order'),
    path('index.html', views.json_list, name='index'),
]
