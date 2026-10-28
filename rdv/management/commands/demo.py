from datetime import timedelta, time
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from rdv.models import Service, Creneau


class Command(BaseCommand):
    help = "Crée des données de démonstration"

    def handle(self, *args, **opts):
        for nom in ["Accueil", "Orientation"]:
            s, _ = Service.objects.get_or_create(nom=nom)
            for j in range(1, 4):
                for h in (9, 10, 11):
                    Creneau.objects.get_or_create(
                        service=s, date=timezone.localdate() + timedelta(days=j),
                        heure_debut=time(h), heure_fin=time(h + 1))
        u, _ = User.objects.get_or_create(username="usager1")
        if not u.has_usable_password() is False and not u.password:
            u.set_unusable_password(); u.save()
        self.stdout.write("OK. Définir le mot de passe : python manage.py changepassword usager1")