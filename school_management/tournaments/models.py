from django.db import models
from points.models import Classes
from django.utils.translation import gettext_lazy as _

class Tournament(models.Model):
    tournament_name = models.CharField(verbose_name=_("Nazwa turnieju"), max_length=100)
    tournament_classes = models.ManyToManyField(Classes, verbose_name=_("Uczestniczące klasy"), null=False, related_name='classes')
    tournament_start_date = models.DateField(verbose_name=_("Data początku"))
    tournament_end_date = models.DateField(verbose_name=_("Data końca"))
    tournament_is_active = models.BooleanField(verbose_name=_("Aktywny (tak/nie)"), default=False)

    def __str__(self) -> str:
        return f"{_(self.tournament_name)}"

class TournamentDay(models.Model):
    tournament = models.ForeignKey(Tournament, verbose_name=_("Turniej"), on_delete=models.CASCADE, null=False)
    day_date = models.DateField(verbose_name=_("Data")) 

    def __str__(self) -> str:
        return f"{_(self.tournament)} - {_(self.day_date)}"


class TournamentBattle(models.Model):
    CHOICES = [
        ("FO", _("Pierwszy przeciwnik")),
        ("SO", _("Drugi przeciwnik"))
    ]
    battle_day = models.ForeignKey(TournamentDay, verbose_name=_("Dzień"), on_delete=models.CASCADE, null=False)
    battle_first_oponent = models.ForeignKey(Classes, verbose_name=_("Pierwszy przeciwnik"),  on_delete=models.CASCADE, related_name="first_oponent", to_field="id")
    battle_second_oponent = models.ForeignKey(Classes, verbose_name=_("Drugi przeciwnik"), on_delete=models.CASCADE, related_name="second_oponent", to_field="id")
    battle_time = models.TimeField(verbose_name=_("Czas pojedynku"))
    battle_is_finished = models.BooleanField(verbose_name=_("Pojedynek skończony"), default=False)
    winner = models.TextField(verbose_name=_("Zwycięzca"), max_length=50, choices=CHOICES, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.battle_day} - {self.battle_time} - Finished: {self.battle_is_finished}"
