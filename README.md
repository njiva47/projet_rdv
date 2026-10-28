# Prise de rendez-vous pour un service (Django)

Application web Django de consultation de créneaux et de réservation de rendez-vous.
Université de Vakinankaratra, M1 GL, Thème 4.

## Prérequis
Python 3.10+ et Git.

## Installation (Windows PowerShell)
```powershell
git clone <URL_DU_DEPOT>
git clone https://github.com/njiva47/projet_rdv.git
cd projet_rdv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Si l'activation est bloquée : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Base de données
La base SQLite `db.sqlite3` est **fournie** avec des données de démonstration :
il n'y a rien à créer, il suffit de lancer le serveur.

Pour repartir d'une base vide (facultatif) :
```powershell
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py demo
python manage.py changepassword usager1
```
(`demo` crée 2 services, des créneaux sur les 3 prochains jours et l'utilisateur `usager1`.)

## Comptes de démonstration
Comptes de test uniquement. Aucun mot de passe n'est écrit dans le code (ils sont hachés dans la base).

| Rôle | Login | Mot de passe |
|---|---|---|
| Gestionnaire / superuser | admin | admin |
| Usager | usager1 | user1234 |
| Usager | usager2 | user1234 |

## Création d'un compte gestionnaire
```powershell
python manage.py createsuperuser
```
Ce compte a le statut équipe (`is_staff`) : il accède à l'agenda, à la création de créneaux et à `/admin/`.
Pour promouvoir un utilisateur existant : `/admin/` → Utilisateurs → cocher « Statut équipe ».

## Lancement
```powershell
python manage.py runserver
```
Ouvrir http://127.0.0.1:8000/

Les créneaux de démo sont datés de quelques jours après leur création. S'ils sont passés,
en recréer avec `python manage.py demo` ou via « Nouveau créneau » (compte gestionnaire).

## Tests
```powershell
python manage.py test
```

## Fonctionnalités
- Liste des créneaux futurs et libres, filtre par service et par date, pagination
- Inscription / connexion, réservation avec motif, espace « Mes rendez-vous »
- Annulation d'un rendez-vous avant son début (avec confirmation)
- Gestionnaire : création de créneaux, agenda filtrable, marquage « réalisé » / « absent »
- Administration Django pour Service, Créneau et RendezVous

## Règles métier
- Un seul rendez-vous « réservé » par créneau (contrainte unique conditionnelle en base)
- Créneau valide : heure de fin après l'heure de début, pas de date passée
- Réservation impossible sur un créneau passé, fermé ou déjà pris
- Annulation uniquement par le propriétaire, avant le début du créneau
- Gestionnaire : transition « réservé » → « réalisé » ou « absent » uniquement

## Structure
- `config/` : configuration du projet
- `rdv/` : modèles, vues, formulaires, tests, commande `demo`
- `templates/` et `static/` : interface
- `requirements.txt` : dépendances