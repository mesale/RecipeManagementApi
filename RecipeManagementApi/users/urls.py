from django.urls import path
from .views import (
    RegisterUserView,
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    UserFavoritesView,
    UserFavoriteDetailView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', UserListCreateView.as_view(), name='users-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='users-detail'),
    path('<int:pk>/favorites/', UserFavoritesView.as_view(), name='users-favorites'),
    path('<int:pk>/favorites/<int:recipe_id>/', UserFavoriteDetailView.as_view(), name='users-favorite-detail'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
