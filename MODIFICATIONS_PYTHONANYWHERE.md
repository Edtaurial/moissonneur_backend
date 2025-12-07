# Modifications nécessaires pour PythonAnywhere

## Modifications dans settings.py

Pour que votre projet fonctionne correctement sur PythonAnywhere, vous devez modifier quelques paramètres dans `plateforme_donnees/settings.py`.

### 1. Ajouter PythonAnywhere aux ALLOWED_HOSTS

Modifiez la section `ALLOWED_HOSTS` pour inclure les domaines PythonAnywhere :

```python
# Render provides the external hostname via env var; include common local hosts, too.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['localhost', '127.0.0.1']

# Ajouter PythonAnywhere
PYTHONANYWHERE_USERNAME = os.environ.get('PYTHONANYWHERE_USERNAME', '')
if PYTHONANYWHERE_USERNAME:
    ALLOWED_HOSTS.append(f'{PYTHONANYWHERE_USERNAME}.pythonanywhere.com')

# Render (garder pour compatibilité)
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

### 2. Ajouter PythonAnywhere aux CSRF_TRUSTED_ORIGINS

Modifiez la section `CSRF_TRUSTED_ORIGINS` :

```python
# Ensure CSRF works on Render domain
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

# Ajouter PythonAnywhere
PYTHONANYWHERE_USERNAME = os.environ.get('PYTHONANYWHERE_USERNAME', '')
if PYTHONANYWHERE_USERNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{PYTHONANYWHERE_USERNAME}.pythonanywhere.com")

# Render (garder pour compatibilité)
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")
```

### 3. Configuration alternative (plus simple)

Si vous préférez une approche plus simple, vous pouvez directement ajouter votre domaine :

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else [
    'localhost', 
    '127.0.0.1',
    'votreusername.pythonanywhere.com'  # Remplacez par votre nom d'utilisateur
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://votreusername.pythonanywhere.com"  # Remplacez par votre nom d'utilisateur
]
```

## Variables d'environnement à configurer sur PythonAnywhere

Dans l'onglet "Web" de PythonAnywhere, section "Environment variables", ajoutez :

- `DEBUG=False`
- `SECRET_KEY=votre-clé-secrète-production` (générez-en une nouvelle avec `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `PYTHONANYWHERE_USERNAME=votreusername` (optionnel, si vous utilisez la méthode dynamique)
- `ALLOWED_HOSTS=votreusername.pythonanywhere.com` (optionnel, si vous utilisez la variable d'environnement)

## Note sur WhiteNoise

Votre projet utilise WhiteNoise pour servir les fichiers statiques. Sur PythonAnywhere, vous pouvez :
- Soit continuer à utiliser WhiteNoise (recommandé)
- Soit utiliser la configuration native de PythonAnywhere pour les fichiers statiques

Les deux méthodes fonctionnent, mais WhiteNoise est plus simple à configurer.

