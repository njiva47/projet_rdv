from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Creneau, RendezVous


class CreneauForm(forms.ModelForm):
    class Meta:
        model = Creneau
        fields = ["service", "date", "heure_debut", "heure_fin", "ouvert"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean_date(self):
        d = self.cleaned_data["date"]
        if d < timezone.localdate():
            raise ValidationError("La date ne peut pas être dans le passé.")
        return d


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ["motif"]


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]