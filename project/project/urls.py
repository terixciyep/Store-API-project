"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path, include

from users.views import ActivateAccount
from .yasg import urlpatterns as swagger_urls
from users.urls import router as user_router
from items.urls import items_router, categories_router
from orders.urls import router as order_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(user_router.urls)),
    path('', include(items_router.urls)),
    path('', include(categories_router.urls)),
    path('', include(order_router.urls)),
    path('verify_email/<uidb64>/<token>/', ActivateAccount.as_view(), name='verify_account'),
    path('', include('social_django.urls', namespace='social'))
] + swagger_urls
