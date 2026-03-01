from rest_framework import serializers
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class IngredientInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class RecipeSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    ingredients = IngredientInputSerializer(many=True, write_only=True)
    ingredient_details = IngredientSerializer(source='ingredients', many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'steps', 'category', 'image',
            'preparation_time', 'cooking_time', 'servings',
            'created_at', 'created_by', 'ingredients', 'ingredient_details'
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            name = ingredient.get('name', '').strip()
            if not name:
                raise serializers.ValidationError({'ingredients': 'Each ingredient must include a non-empty name.'})
            ing_obj, created = Ingredient.objects.get_or_create(name=name)
            recipe.ingredients.add(ing_obj)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ingredients_data is not None:
            instance.ingredients.clear()
            for ingredient in ingredients_data:
                name = ingredient.get('name', '').strip()
                if not name:
                    raise serializers.ValidationError({'ingredients': 'Each ingredient must include a non-empty name.'})
                ing_obj, created = Ingredient.objects.get_or_create(name=name)
                instance.ingredients.add(ing_obj)
        return instance
