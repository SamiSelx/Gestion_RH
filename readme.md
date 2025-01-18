# Gestion des Ressources Humaines d'une Entreprise

## Description du Projet
Ce projet vise à créer une application web de gestion des ressources humaines pour une entreprise en utilisant le framework Django avec des templates HTML. L'application centralise et automatise divers processus RH tels que la gestion des employés, des congés, des salaires, et des recrutements.

## Bibliothèques Utilisées
- **xhtml2pdf** : Utilisé pour générer des fichiers PDF à partir des données de l'application.
- **six** : Fournit une compatibilité entre Python 2 et Python 3 pour certaines opérations.

## Installation et Exécution de l'Application

1. **Cloner le dépôt GitHub**
   ```bash
   git clone https://github.com/SamiSelx/Gestion_RH
   cd Gestion-RH/gestion_RH
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv env
   source env\Scripts\activate   # Sous Linux : env/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations de la base de données**
   ```bash
   python manage.py migrate
   ```

5. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

6. **Accéder à l'application**
   Ouvrez un navigateur et accédez à : [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Fonctionnalités de l'Application
- **Système de rôles** : Gestion des permissions basée sur les rôles attribués aux utilisateurs (Employé, Candidat, RH, Manager).
- **Gestion automatisée** : Pages dédiées pour chaque rôle afin de simplifier les processus RH.
- **Génération de documents** : Création de fiche de paie en format PDF.

## Aperçu Technique
L'application suit les bonnes pratiques de développement Django, avec une architecture bien structurée pour assurer la maintenabilité et l'évolutivité.



