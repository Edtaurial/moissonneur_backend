# Guide de déploiement sur PythonAnywhere.com

Ce guide vous explique comment héberger votre projet Django sur PythonAnywhere.

## Prérequis

1. Un compte sur [PythonAnywhere.com](https://www.pythonanywhere.com) (gratuit ou payant)
2. Votre projet Django prêt à être déployé
3. Git installé localement (pour pousser votre code)

## Étape 1 : Préparer votre projet localement

### 1.1 Créer un fichier .gitignore (si pas déjà présent)

Assurez-vous que votre `.gitignore` inclut :
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
db.sqlite3
db.sqlite3-journal
staticfiles/
*.log
.env
```

### 1.2 Vérifier les settings pour la production

Votre fichier `settings.py` doit être configuré pour la production. Vérifiez que :
- `DEBUG = False` en production (ou via variable d'environnement)
- `ALLOWED_HOSTS` contient votre domaine PythonAnywhere
- Les fichiers statiques sont correctement configurés

## Étape 2 : Créer un compte et accéder à PythonAnywhere

1. Allez sur [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Créez un compte gratuit (Beginner) ou payant
3. Connectez-vous à votre compte

## Étape 3 : Uploader votre code

### Option A : Via Git (Recommandé)

1. **Sur votre machine locale**, poussez votre code sur GitHub/GitLab/Bitbucket :
   ```bash
   git add .
   git commit -m "Préparation pour déploiement"
   git push origin master
   ```

2. **Sur PythonAnywhere**, dans l'onglet "Consoles" :
   - Ouvrez un Bash console
   - Clonez votre repository :
     ```bash
     cd ~
     git clone https://github.com/votre-username/votre-repo.git
     cd votre-repo/plateforme_donnees
     ```

### Option B : Via l'interface web

1. Dans l'onglet "Files", naviguez vers `/home/votreusername/`
2. Utilisez l'option "Upload a file" pour uploader vos fichiers
3. Ou utilisez l'éditeur pour créer/copier vos fichiers

## Étape 4 : Configurer l'environnement Python

1. **Dans l'onglet "Web"**, cliquez sur "Add a new web app"
2. Choisissez "Manual configuration" (pas Flask)
3. Sélectionnez Python 3.10 ou 3.11 (selon disponibilité)

## Étape 5 : Installer les dépendances

1. **Dans l'onglet "Consoles"**, ouvrez un Bash console
2. Naviguez vers votre projet :
   ```bash
   cd ~/votre-repo/plateforme_donnees
   ```
3. Créez un environnement virtuel (optionnel mais recommandé) :
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```
4. Installez les dépendances :
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
   
   **Note importante** : PythonAnywhere a des restrictions sur certains packages. Si `psycopg2-binary` pose problème (pour PostgreSQL), vous pouvez le retirer du requirements.txt si vous utilisez SQLite.

## Étape 6 : Configurer la base de données

### Pour SQLite (défaut actuel)

1. Dans le Bash console :
   ```bash
   cd ~/votre-repo/plateforme_donnees
   python3.10 manage.py migrate
   python3.10 manage.py createsuperuser
   ```

### Pour MySQL (recommandé pour la production)

1. Dans l'onglet "Databases", créez une base de données MySQL
2. Notez les identifiants :
   - **Database name** : `votreusername$plateforme_donnees` (format automatique)
   - **Username** : votre nom d'utilisateur PythonAnywhere
   - **Password** : le mot de passe que vous avez défini
   - **Hostname** : `localhost` (pour comptes gratuits) ou `votreusername.mysql.pythonanywhere-services.com`
3. Créez un fichier `.env` dans votre projet (voir Étape 9) et ajoutez :
   - `DB_NAME=votreusername$plateforme_donnees`
   - `DB_USER=votreusername`
   - `DB_PASSWORD=votre_mot_de_passe`
   - `DB_HOST=localhost` (ou `votreusername.mysql.pythonanywhere-services.com`)
   - `DB_PORT=3306`
   - `PYTHONANYWHERE_USERNAME=votreusername`
4. Le fichier `settings.py` détecte automatiquement PythonAnywhere et utilise MySQL
5. Installez le driver MySQL si nécessaire :
   ```bash
   pip3.10 install --user mysqlclient
   ```
6. Exécutez les migrations :
   ```bash
   python3.10 manage.py migrate
   python3.10 manage.py createsuperuser
   ```

**Note** : Consultez `CONFIGURATION_MYSQL_PYTHONANYWHERE.md` pour plus de détails.

## Étape 7 : Collecter les fichiers statiques

```bash
cd ~/votre-repo/plateforme_donnees
python3.10 manage.py collectstatic --noinput
```

## Étape 8 : Configurer le fichier WSGI

1. **Dans l'onglet "Web"**, cliquez sur le lien "WSGI configuration file"
2. Remplacez le contenu par :

```python
import os
import sys

# Ajoutez le chemin de votre projet au PYTHONPATH
path = '/home/votreusername/votre-repo/plateforme_donnees'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurez le module de settings Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'plateforme_donnees.settings'

# Importez l'application WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important** : 
- Remplacez `votreusername` par votre nom d'utilisateur PythonAnywhere et `votre-repo` par le nom de votre dossier de projet.
- Le fichier `wsgi.py` de votre projet charge déjà automatiquement le fichier `.env`, donc vous n'avez pas besoin de le modifier dans le WSGI de PythonAnywhere si vous utilisez le fichier `.env`.

## Étape 9 : Configurer les variables d'environnement

PythonAnywhere utilise un fichier `.env` pour les variables d'environnement. Voici comment le configurer :

1. **Dans un Bash console**, naviguez vers votre projet :
   ```bash
   cd ~/votre-repo/plateforme_donnees
   ```

2. **Créez un fichier `.env`** :
   ```bash
   nano .env
   ```
   
   Ou utilisez l'éditeur de fichiers dans l'onglet "Files" de PythonAnywhere.

3. **Ajoutez les variables suivantes** (remplacez par vos valeurs) :
   ```
   DEBUG=False
   SECRET_KEY=votre-clé-secrète-production
   PYTHONANYWHERE_USERNAME=votreusername
   ALLOWED_HOSTS=votreusername.pythonanywhere.com,localhost,127.0.0.1
   ```

4. **Si vous utilisez MySQL**, ajoutez aussi :
   ```
   DB_NAME=votreusername$plateforme_donnees
   DB_USER=votreusername
   DB_PASSWORD=votre_mot_de_passe_mysql
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. **Générez une clé secrète** si vous n'en avez pas :
   ```bash
   python3.10 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

**Note** : Le fichier `wsgi.py` a été configuré pour charger automatiquement le fichier `.env`. Consultez `env.example` pour un modèle.

## Étape 10 : Configurer les fichiers statiques et médias

1. **Dans l'onglet "Web"**, dans la section "Static files"
2. Ajoutez :
   - **URL** : `/static/`
   - **Directory** : `/home/votreusername/votre-repo/plateforme_donnees/staticfiles/`

## Étape 11 : Mettre à jour ALLOWED_HOSTS dans settings.py

Modifiez votre fichier `settings.py` pour inclure votre domaine PythonAnywhere :

```python
ALLOWED_HOSTS = ['votreusername.pythonanywhere.com', 'localhost', '127.0.0.1']
```

Ou utilisez une variable d'environnement (recommandé) :

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['localhost', '127.0.0.1']
```

## Étape 12 : Relancer l'application

1. **Dans l'onglet "Web"**, cliquez sur le bouton vert **"Reload"**
2. Attendez quelques secondes
3. Visitez votre site : `https://votreusername.pythonanywhere.com`

## Étape 13 : Vérifier les logs en cas d'erreur

Si quelque chose ne fonctionne pas :

1. **Dans l'onglet "Web"**, consultez :
   - **Error log** : pour les erreurs serveur
   - **Server log** : pour les logs généraux

## Configuration supplémentaire

### Pour GraphQL

Si vous utilisez GraphQL, assurez-vous que le chemin est correctement configuré dans `plateforme_donnees/urls.py`.

### Pour les tâches planifiées (cron jobs)

Si vous avez des commandes de management à exécuter régulièrement :

1. **Dans l'onglet "Tasks"**, créez une tâche planifiée
2. Exemple pour exécuter la commande `moissonner` tous les jours :
   ```bash
   cd /home/votreusername/votre-repo/plateforme_donnees && python3.10 manage.py moissonner
   ```

### Pour les fichiers de log

Les logs Django seront dans :
```
/home/votreusername/votre-repo/plateforme_donnees/logs/
```

## Dépannage courant

### Erreur 500
- Vérifiez les logs d'erreur dans l'onglet "Web"
- Vérifiez que `DEBUG=False` en production
- Vérifiez que `ALLOWED_HOSTS` contient votre domaine

### Fichiers statiques non chargés
- Vérifiez que `collectstatic` a été exécuté
- Vérifiez la configuration des fichiers statiques dans l'onglet "Web"
- Vérifiez que `STATIC_ROOT` est correctement défini

### Erreurs d'import
- Vérifiez que tous les packages sont installés
- Vérifiez le chemin dans le fichier WSGI
- Vérifiez que le PYTHONPATH est correct

### Base de données verrouillée (SQLite)
- SQLite peut avoir des problèmes en production avec plusieurs processus
- Considérez l'utilisation de MySQL (gratuit sur PythonAnywhere)

## Mise à jour de votre application

Pour mettre à jour votre application après des changements :

1. Dans le Bash console :
   ```bash
   cd ~/votre-repo/plateforme_donnees
   git pull  # si vous utilisez Git
   python3.10 manage.py migrate  # si vous avez de nouvelles migrations
   python3.10 manage.py collectstatic --noinput  # si vous avez changé les fichiers statiques
   ```

2. Dans l'onglet "Web", cliquez sur **"Reload"**

## Limitations du compte gratuit

- 1 application web
- Domaine : `votreusername.pythonanywhere.com`
- Pas de HTTPS personnalisé (mais HTTPS est disponible)
- Limite de CPU et de trafic
- Pas d'accès SSH complet

## Ressources utiles

- [Documentation PythonAnywhere](https://help.pythonanywhere.com/)
- [Guide Django sur PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Forum PythonAnywhere](https://www.pythonanywhere.com/forums/)

## Notes importantes

1. **Ne commitez jamais** `db.sqlite3` ou vos fichiers de secrets dans Git
2. Utilisez des variables d'environnement pour les secrets en production
3. Le compte gratuit a des limitations - considérez un compte payant pour la production
4. PythonAnywhere redémarre automatiquement votre application chaque jour à minuit (heure UTC)

