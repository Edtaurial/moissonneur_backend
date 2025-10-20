from django.urls import path
from .views import JeuDeDonneesListAPIView, JeuDeDonneesDetailAPIView

urlpatterns = [
    path('api/jeuxdedonnees/', JeuDeDonneesListAPIView.as_view(), name='jeudedonnees-list'),
    path('api/jeuxdedonnees/<int:pk>/', JeuDeDonneesDetailAPIView.as_view(), name='jeudedonnees-detail'),
]