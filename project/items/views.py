from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from items.models import Item, Category
from items.serializers import ItemSerializer, CategorySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer