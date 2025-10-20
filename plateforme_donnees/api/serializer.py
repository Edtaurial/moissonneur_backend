from rest_framework import serializers
from moissonneur.models import JeuDeDonnees

class JeuDeDonneesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JeuDeDonnees
        fields = '__all__'