# Configuration MySQL sur PythonAnywhere

Ce guide vous explique comment configurer MySQL pour votre projet Django sur PythonAnywhere.

## Étape 1 : Créer la base de données MySQL sur PythonAnywhere

1. **Connectez-vous à votre compte PythonAnywhere**
2. **Allez dans l'onglet "Databases"**
3. **Cliquez sur "Create a new MySQL database"** (ou utilisez une base existante)
4. **Notez les informations suivantes** :
   - **Database name** : `votreusername$nom_de_la_base` (ex: `monuser$plateforme_donnees`)
   - **Username** : `votreusername` (généralement votre nom d'utilisateur PythonAnywhere)
   - **Password** : Le mot de passe que vous avez défini
   - **Hostname** : `votreusername.mysql.pythonanywhere-services.com` (ou `localhost` pour les comptes gratuits)

## Étape 2 : Installer le driver MySQL

Sur PythonAnywhere, dans un Bash console :

```bash
pip3.10 install --user mysqlclient
```

**Note** : `mysqlclient` est généralement pré-installé sur PythonAnywhere, mais si vous avez des erreurs, installez-le.

## Étape 3 : Configurer settings.py

Votre fichier `settings.py` a été modifié pour détecter automatiquement PythonAnywhere et utiliser MySQL. 

### Configuration automatique (recommandée)

Le `settings.py` modifié détecte automatiquement si vous êtes sur PythonAnywhere en vérifiant :
- La variable d'environnement `PYTHONANYWHERE_USERNAME`
- Ou la présence de `pythonanywhere.com` dans le hostname

### Configuration manuelle avec fichier .env

PythonAnywhere utilise un fichier `.env` pour les variables d'environnement. Créez ce fichier dans votre projet :

1. **Dans un Bash console** :
   ```bash
   cd ~/votre-repo/plateforme_donnees
   nano .env
   ```

2. **Ajoutez les variables suivantes** :
   ```
   DB_NAME=votreusername$nom_de_la_base
   DB_USER=votreusername
   DB_PASSWORD=votre_mot_de_passe
   DB_HOST=localhost
   DB_PORT=3306
   PYTHONANYWHERE_USERNAME=votreusername
   ```

3. **Sauvegardez le fichier** (Ctrl+X, puis Y, puis Enter dans nano)

**Note** : Le fichier `wsgi.py` charge automatiquement le fichier `.env`, donc ces variables seront disponibles pour votre application.

## Étape 4 : Migrer la base de données

1. **Dans un Bash console sur PythonAnywhere** :
   ```bash
   cd ~/votre-repo/plateforme_donnees
   python3.10 manage.py migrate
   ```

2. **Créer un superutilisateur** :
   ```bash
   python3.10 manage.py createsuperuser
   ```

## Étape 5 : Migrer les données depuis SQLite (optionnel)

Si vous avez déjà des données dans SQLite et que vous voulez les transférer :

1. **Sur votre machine locale**, exportez les données :
   ```bash
   python manage.py dumpdata > data.json
   ```

2. **Sur PythonAnywhere**, après avoir configuré MySQL et fait les migrations :
   ```bash
   python3.10 manage.py loaddata data.json
   ```

## Dépannage

### Erreur : "No module named 'MySQLdb'"

Installez mysqlclient :
```bash
pip3.10 install --user mysqlclient
```

### Erreur : "Access denied for user"

Vérifiez :
- Le nom d'utilisateur est correct (généralement votre nom d'utilisateur PythonAnywhere)
- Le mot de passe est correct
- Le nom de la base de données est correct (format : `username$dbname`)

### Erreur : "Unknown database"

Assurez-vous que la base de données a été créée dans l'onglet "Databases" de PythonAnywhere.

### Erreur de connexion

Pour les comptes gratuits, utilisez `localhost` comme hostname au lieu de `votreusername.mysql.pythonanywhere-services.com`.

## Vérification

Pour vérifier que tout fonctionne :

```bash
python3.10 manage.py dbshell
```

Vous devriez voir le prompt MySQL. Tapez `exit` pour quitter.

## Avantages de MySQL sur SQLite

- ✅ Meilleure performance avec plusieurs utilisateurs simultanés
- ✅ Pas de problèmes de verrouillage de fichier
- ✅ Meilleur pour la production
- ✅ Support des transactions plus robuste
- ✅ Gratuit sur PythonAnywhere (comptes Beginner et Hacker)

