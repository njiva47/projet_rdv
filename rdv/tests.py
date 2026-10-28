from datetime import timedelta, time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Service, Creneau, RendezVous


class RdvTests(TestCase):
    def setUp(self):
        s = Service.objects.create(nom="Accueil")
        self.c = Creneau.objects.create(service=s, date=timezone.localdate() + timedelta(days=1),
                                        heure_debut=time(9), heure_fin=time(10))
        self.u1 = User.objects.create_user("u1")
        self.u2 = User.objects.create_user("u2")

    def test_validation_heures(self):  # validation de données
        c = Creneau(service=self.c.service, date=self.c.date, heure_debut=time(10), heure_fin=time(9))
        with self.assertRaises(ValidationError):
            c.full_clean()

    def test_pas_de_double_reservation(self):  # règle métier
        for u in (self.u1, self.u2):
            self.client.force_login(u)
            self.client.post(reverse("reserver", args=[self.c.pk]), {"motif": "Info"})
        self.assertEqual(RendezVous.objects.filter(statut="reserve").count(), 1)

    def test_agenda_interdit_aux_non_gestionnaires(self):  # restriction d'accès
        self.client.force_login(self.u1)
        self.assertEqual(self.client.get(reverse("agenda")).status_code, 403)

    def test_annulation_rdv_d_un_autre(self):  # droits
        r = RendezVous.objects.create(creneau=self.c, utilisateur=self.u1, motif="x")
        self.client.force_login(self.u2)
        self.assertEqual(self.client.post(reverse("annuler", args=[r.pk])).status_code, 404)