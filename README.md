# Prise de rendez-vous pour un service (Django)

Application web Django de consultation de créneaux et de réservation de rendez-vous.
Université de Vakinankaratra, M1 GL, Thème 4.

## Prérequis
Python 3.10+ et Git.

## Installation (Windows PowerShell)
```powershell
git clone https://github.com/njiva47/projet_rdv.git
cd projet_rdv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Si l'activation est bloquée : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Base de données et données de démonstration
La base SQLite n'est pas versionnée. Pour la créer et la peupler :
```powershell
python manage.py migrate
python manage.py demo --admin-password admin --user-password user1234
```
La commande `demo` crée 3 services, des créneaux sur 14 jours (hors week-ends), 2 rendez-vous
d'exemple et les comptes ci-dessous. Elle peut être relancée sans créer de doublons
(utile pour regénérer des créneaux futurs le jour de la correction).

Options : `--jours N` pour changer le nombre de jours de créneaux (14 par défaut).
Aucun mot de passe n'est écrit dans le code : ils sont passés en ligne de commande.

## Comptes de démonstration
Comptes de test uniquement, créés par la commande `demo`.

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

## Tests
```powershell
python manage.py test
```
5 tests : validation des heures, double réservation, accès à l'agenda, annulation du rendez-vous
d'un autre, gestionnaire ne pouvant pas réserver.

## Fonctionnalités
- Liste des créneaux futurs et libres, filtre par service et par date, pagination
- Inscription / connexion, réservation avec motif, espace « Mes rendez-vous »
- Annulation d'un rendez-vous avant son début (avec confirmation)
- Gestionnaire : création de créneaux, agenda filtrable, marquage « réalisé » / « absent »
- Le gestionnaire ne réserve pas : il gère les créneaux et suit les rendez-vous
- Administration Django pour Service, Créneau et RendezVous

## Règles métier
- Un seul rendez-vous « réservé » par créneau (contrainte unique conditionnelle en base)
- Créneau valide : heure de fin après l'heure de début, pas de date passée
- Réservation impossible sur un créneau passé, fermé ou déjà pris
- Réservation réservée aux utilisateurs non gestionnaires
- Annulation uniquement par le propriétaire, avant le début du créneau
- Gestionnaire : transition « réservé » → « réalisé » ou « absent » uniquement

## Structure
- `config/` : configuration du projet
- `rdv/` : modèles, vues, formulaires, tests, commande `demo`
- `templates/` et `static/` : interface
- `requirements.txt` : dépendances