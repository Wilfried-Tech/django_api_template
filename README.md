# Django API Boilerplate Template

Un template de base pour créer des APIs RESTful avec Django et Django REST Framework. Ce template fournit une base solide pour créer des APIs évolutives et maintenables en suivant les meilleures pratiques.

## ✨ Fonctionnalités

- **Django 5.2.5** avec Django REST Framework 3.16.1
- **Authentification JWT** avec refresh tokens et blacklisting
- **Authentification personnalisée** avec support des cookies et JWT
- **CamelCase API** - Conversion automatique des noms de champs
- **Documentation API** automatique avec Swagger/ReDoc (drf-spectacular)
- **Gestion des erreurs standardisées** avec drf-standardized-errors
- **CORS** configuré pour le développement et la production
- **Pagination** personnalisée avec taille de page configurable
- **Filtrage** avec django-filter
- **Throttling** configuré pour les endpoints sensibles
- **Modèle utilisateur personnalisé** avec email comme identifiant
- **Gestion des fichiers statiques** avec WhiteNoise
- **Debug Toolbar** pour le développement
- **Commande de création d'admin** automatisée
- **Configuration multi-environnements** (development/production)

## 🛠️ Stack Technique

### Backend
- **Django** 5.2.5
- **Django REST Framework** 3.16.1
- **Simple JWT** pour l'authentification
- **drf-spectacular** pour la documentation API

### Base de données
- **SQLite** par défaut (configurable avec DATABASE_URL)
- Support PostgreSQL, MySQL via dj-database-url

### Utilitaires
- **WhiteNoise** pour les fichiers statiques
- **django-cors-headers** pour CORS
- **django-filter** pour le filtrage
- **Pillow** pour la gestion d'images
- **python-decouple** pour la configuration d'environnement

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- pip ou pipenv

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd django_api_template
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration d'environnement

Créez un fichier `.env` à la racine du projet en vous basant sur `.env.example` :

```bash
# Django Settings
DEBUG=True
SECRET_KEY=votre-clé-secrète-très-sécurisée
DJANGO_SETTINGS_MODULE=config.settings.development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optionnel, SQLite par défaut)
DATABASE_URL=sqlite:///db.sqlite3
# Pour PostgreSQL: DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Redis (optionnel)
REDIS_URL=redis://localhost:6379/0
REDIS_ENABLED=False

# CORS (pour le développement)
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email (pour le développement, utilise la console par défaut)
EMAIL_HOST_USER=votre-email@exemple.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe

# Security (pour la production)
SECURE_SSL_ENABLED=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### 5. Migrations et configuration initiale
```bash
# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur automatiquement
python manage.py create_default_admin

# Ou créer un superutilisateur manuellement
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```

## 📚 Documentation API

Une fois le serveur lancé, vous pouvez accéder à la documentation API :

- **Swagger UI** : http://127.0.0.1:8000/docs/
- **ReDoc** : http://127.0.0.1:8000/docs/redoc/
- **Schéma JSON** : http://127.0.0.1:8000/api/schema/

## 🔐 Authentification

L'API utilise l'authentification JWT avec les endpoints suivants :

- `POST /api/auth/login/` - Connexion (retourne access et refresh tokens)
- `POST /api/auth/refresh/` - Renouvellement du token d'accès
- `POST /api/auth/logout/` - Déconnexion (blacklist le refresh token)
- `POST /api/auth/register/` - Inscription d'un nouvel utilisateur
- `POST /api/auth/password-reset/` - Réinitialisation de mot de passe

### Configuration JWT
- **Access Token** : 15 minutes de validité
- **Refresh Token** : 7 jours de validité
- **Rotation automatique** des refresh tokens
- **Blacklisting** après rotation pour sécurité

## 🏗️ Structure du Projet

```
django_api_template/
├── apps/
│   └── accounts/          # Application de gestion des utilisateurs
│       ├── authentication.py    # Classes d'authentification personnalisées
│       ├── models.py           # Modèle User personnalisé
│       ├── serializers.py     # Sérialiseurs pour l'API
│       ├── views.py           # Vues API
│       ├── urls.py           # URLs de l'application
│       ├── permissions.py    # Permissions personnalisées
│       ├── throttles.py      # Limiteurs de taux
│       └── management/commands/
│           └── create_default_admin.py
├── config/
│   ├── settings/
│   │   ├── base.py           # Configuration de base
│   │   ├── development.py    # Configuration développement
│   │   └── production.py     # Configuration production
│   ├── urls.py              # URLs principales
│   ├── router.py            # Router API
│   └── pagination.py        # Classes de pagination
├── utils/                   # Utilitaires partagés
├── requirements.txt         # Dépendances Python
├── manage.py               # Script de gestion Django
└── .env.example           # Exemple de configuration
```

## 🔧 Configuration pour le Développement

### Variables d'environnement importantes

```bash
# Activer le mode debug
DEBUG=True

# Configuration pour le développement local
DJANGO_SETTINGS_MODULE=config.settings.development

# Permettre tous les hôtes (développement uniquement)
ALLOWED_HOSTS=*

# CORS permissif pour le développement
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
```

### Fonctionnalités de développement activées

- **Debug Toolbar** : Barre d'outils de débogage Django
- **Console Email Backend** : Les emails sont affichés dans la console
- **Authentifications multiples** : Session, Token, Basic auth en plus de JWT
- **API Browsable** : Interface web pour tester l'API
- **CORS permissif** : Autorise toutes les origines

### Commandes utiles pour le développement

```bash
# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur par défaut
python manage.py create_default_admin

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test

# Shell Django avec extensions
python manage.py shell_plus

# Réinitialiser la base de données
python manage.py flush
```

## 🔐 Sécurité

### Fonctionnalités de sécurité incluses

- **Authentification JWT** avec rotation des tokens
- **Blacklisting** des refresh tokens
- **Throttling** sur les endpoints sensibles
- **Validation des mots de passe** robuste
- **CORS** configuré de manière sécurisée
- **Gestion des erreurs** standardisée sans exposition d'informations sensibles

### Pour la production

Assurez-vous de configurer ces variables dans votre `.env` de production :

```bash
DEBUG=False
SECRET_KEY=une-clé-très-sécurisée-et-unique
SECURE_SSL_ENABLED=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
