from django.urls import path
from .views import CategoryListView, CategoryDetailView, FavoriteView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<str:pk>/', CategoryDetailView.as_view()),
    path('favorite/', FavoriteView.as_view()),
]