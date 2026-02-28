from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or request.user.id == obj.id)


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not (request.user.is_staff or request.user.id == user.id):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        recipes = user.favorite_recipes.all()
        serializer = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not (request.user.is_staff or request.user.id == user.id):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        recipe_id = request.data.get("recipe_id")
        if not recipe_id:
            return Response(
                {"detail": "recipe_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.favorited_by.add(user)
        return Response({"message": "Added to favorites"}, status=status.HTTP_200_OK)
