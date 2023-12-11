from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children_cat')

    def __str__(self):
        if self.categories:
            return f"{self.name} | {self.categories}"
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(to=Category, related_name='cat_of_item')

    def __str__(self):
        return self.name
