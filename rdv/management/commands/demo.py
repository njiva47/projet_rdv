from datetime import time, timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from rdv.models import Creneau, RendezVous, Service

SERVICES = {
    "Accueil": "Informations générales et orientation",
    "Orientation": "Entretien de conseil et de suivi",
    "Inscription": "Aide aux démarches administratives",
}
HEURES = [9, 10, 11, 14, 15]


class Command(BaseCommand):
    help = "Peuple la base avec des données de démonstration (peut être relancée sans doublons)"

    def add_arguments(self, parser):
        parser.add_argument("--admin-password", help="mot de passe du compte admin")
        parser.add_argument("--user-password", help="mot de passe de usager1 et usager2")
        parser.add_argument("--jours", type=int, default=14, help="nombre de jours de créneaux")

    def creer_user(self, nom, mdp, staff=False):
        u, cree = User.objects.get_or_create(username=nom)
        if staff:
            u.is_staff = u.is_superuser = True
        if mdp:
            u.set_password(mdp)
        elif cree:
            u.set_unusable_password()
        u.save()
        return u

    def handle(self, *args, **o):
        self.creer_user("admin", o["admin_password"], staff=True)
        u1 = self.creer_user("usager1", o["user_password"])
        u2 = self.creer_user("usager2", o["user_password"])

        aujourd_hui = timezone.localdate()
        for nom, desc in SERVICES.items():
            service, _ = Service.objects.get_or_create(nom=nom, defaults={"description": desc})
            for j in range(1, o["jours"] + 1):
                d = aujourd_hui + timedelta(days=j)
                if d.weekday() >= 5:  # pas de week-end
                    continue
                for h in HEURES:
                    Creneau.objects.get_or_create(
                        service=service, date=d,
                        heure_debut=time(h), heure_fin=time(h + 1))

        # quelques rendez-vous pour l'agenda
        libres = Creneau.objects.filter(service__nom="Accueil", rendezvous__isnull=True)[:2]
        motifs = ["Renseignements sur une inscription", "Dépôt de documents"]
        for u, c, m in zip((u1, u2), libres, motifs):
            RendezVous.objects.create(creneau=c, utilisateur=u, motif=m)

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées."))