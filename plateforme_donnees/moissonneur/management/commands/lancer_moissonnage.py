import requests
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from moissonneur.models import JeuDeDonnees

# L'URL de l'API CKAN pour la recherche de jeux de données (package_search)
# CORRIGÉ : L'URL est maintenant une chaîne de caractères simple.
API_URL = "https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search"
SOURCE_CATALOGUE = "CanWin"


class Command(BaseCommand):
    help = 'Lance le moissonnage des données depuis le catalogue CanWin.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Début du moissonnage pour CanWin ---'))

        try:
            # Faire l'appel à l'API
            response = requests.get(API_URL)
            response.raise_for_status()  # Lève une exception si le statut HTTP est une erreur (4xx ou 5xx)
            data = response.json()

            # Vérifier que la réponse de l'API est correcte
            if data.get('success'):
                jeux_de_donnees = data.get('result', {}).get('results', [])
                compteur_creation = 0
                compteur_maj = 0

                for item in jeux_de_donnees:
                    # Pour chaque jeu de données, on le crée s'il n'existe pas,
                    # ou on le met à jour s'il existe déjà.
                    # On se base sur le champ 'id_source' qui est unique.

                    jeu, created = JeuDeDonnees.objects.update_or_create(
                        id_source=item.get('id'),
                        defaults={
                            'titre': item.get('title', 'Titre non disponible'),
                            'description': item.get('notes', ''),
                            'source_catalogue': SOURCE_CATALOGUE,
                            'url_source': f"[https://canwin-datahub.ad.umanitoba.ca/dataset/](https://canwin-datahub.ad.umanitoba.ca/dataset/){item.get('name')}",
                            'organisation': item.get('organization', {}).get('title',
                                                                             'Organisation non spécifiée') if item.get(
                                'organization') else 'Organisation non spécifiée',

                            # On convertit les dates (format texte) en objets DateTime
                            # Le .get() évite les erreurs si les dates sont absentes
                            'date_creation_source': parse_datetime(item.get('metadata_created')) if item.get(
                                'metadata_created') else None,
                            'date_modification_source': parse_datetime(item.get('metadata_modified')) if item.get(
                                'metadata_modified') else None,
                        }
                    )

                    if created:
                        compteur_creation += 1
                        self.stdout.write(f"  [CRÉÉ] {jeu.titre}")
                    else:
                        compteur_maj += 1
                        self.stdout.write(f"  [MIS À JOUR] {jeu.titre}")

                self.stdout.write(self.style.SUCCESS(f'--- Moissonnage terminé ---'))
                self.stdout.write(f'{compteur_creation} jeux de données créés.')
                self.stdout.write(f'{compteur_maj} jeux de données mis à jour.')

            else:
                self.stdout.write(self.style.ERROR('L\'API a retourné une erreur.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erreur de connexion à l\'API : {e}'))
