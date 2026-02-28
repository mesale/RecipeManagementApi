from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class IsCreatorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.created_by_id == request.user.id


class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.user in recipe.favorited_by.all():
            recipe.favorited_by.remove(request.user)
            return Response({"message": "Removed from favorites"}, status=200)
        else:
            recipe.favorited_by.add(request.user)
            return Response({"message": "Added to favorites"}, status=200)


class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description', 'ingredients__name']
    ordering_fields = ['preparation_time', 'cooking_time', 'servings', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Recipe.objects.all()
        favorite = self.request.query_params.get('favorite')
        ingredients = self.request.query_params.getlist('ingredient')

        if len(ingredients) == 1 and ',' in ingredients[0]:
            ingredients = [item.strip() for item in ingredients[0].split(',') if item.strip()]

        if favorite == 'true':
            queryset = queryset.filter(favorited_by=self.request.user)

        for ingredient in ingredients:
            queryset = queryset.filter(ingredients__name__icontains=ingredient)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrAdmin]
