from rest_framework import serializers

from items.models import Item, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class RecursiveCategorySerializer(serializers.ModelSerializer):
    children_cat = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'children_cat')

    def get_children_cat(self, obj):
        children = Category.objects.filter(categories=obj)
        serializer = RecursiveCategorySerializer(children, many=True)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    children_cat = RecursiveCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'children_cat')