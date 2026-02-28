from django.db import models
from django.conf import settings

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('dessert', 'Dessert'),
        ('main', 'Main Course'),
        ('breakfast', 'Breakfast'),
        ('vegetarian', 'Vegetarian'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    steps = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.URLField(blank=True, null=True)
    preparation_time = models.IntegerField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_recipes',
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title
