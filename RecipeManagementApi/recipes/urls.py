from django.urls import path
from .views import RecipeListCreateView, RecipeRetrieveUpdateDestroyView, ToggleFavoriteView

urlpatterns = [
    path('', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view(), name='recipe-detail'),
    path('<int:pk>/favorite/', ToggleFavoriteView.as_view()),
]