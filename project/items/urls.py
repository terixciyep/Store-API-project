from rest_framework.routers import DefaultRouter

from items.views import ItemViewSet, CategoryViewSet

items_router = DefaultRouter()
categories_router = DefaultRouter()


items_router.register(r'items', ItemViewSet, basename='items')
categories_router.register(r'categories', CategoryViewSet, basename='items')