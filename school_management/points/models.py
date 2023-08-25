from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Classes(models.Model):
    SCHOOL_LETTER_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    # TODO: Do it automatically
    SCHOOL_LEVEL_CHOICES = [
        (_("Klasy początkowe"), _("Klasy początkowe")),
        (_("Klasy średnie"), _("Klasy średnie")),
        (_("Klasy starsze"), _("Klasy starsze")),
    ]

    class_number = models.PositiveSmallIntegerField(verbose_name=_("Numer klasy"),
        validators=[MinValueValidator(1), MaxValueValidator(12)], null=False
    )
    class_letter = models.CharField(verbose_name=_("Litera klasy"),
        max_length=1, choices=SCHOOL_LETTER_CHOICES, default="A"
    )
    class_school_level = models.CharField(_("Poziom szkolnictwa"),
        max_length=16, choices=SCHOOL_LEVEL_CHOICES, default="Klasy średnie"
    )
    class_teacher_name = models.CharField(verbose_name=_("Imię wychowawczyni"), max_length=20)
    class_teacher_surname = models.CharField(verbose_name=_("Nazwisko wychowawczyni"), max_length=20)
    class_points = models.PositiveSmallIntegerField(verbose_name=_("Punkty"),
        validators=[MinValueValidator(0), MaxValueValidator(999)], null=False,
        default=0
    )

    def __str__(self):
        return f"{self.class_number}{str(self.class_letter).capitalize()} - {_(self.class_school_level)}"


class Article(models.Model):
    title = models.CharField(verbose_name=_("Nazwa tytułowa"), max_length=50)
    cover_photo = models.ImageField(verbose_name=_("Zdjęcie główne"))
    description = models.TextField(verbose_name=_("Tekst"))
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _(self.title)
    

class Photo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Zdjęcie"))

    def __str__(self):
        return f"{_(self.article.title)} - {self.photo.url}"


class PointsLog(models.Model):
    points_log_class = models.ForeignKey(Classes, verbose_name=_("Klasa rejestru"), on_delete=models.CASCADE, null=True)
    points_log_date = models.DateField(verbose_name=_("Data rejestru"), auto_now_add=True)
    points_log_type = models.BooleanField(verbose_name=_("Typ rejestru"), null=True, blank=True)
    points_log_amount = models.PositiveSmallIntegerField(verbose_name=_("Ilość punktów"),
        validators=[MinValueValidator(1), MaxValueValidator(100)], null=False
    )
    points_log_created_by = models.CharField(verbose_name=_("Przez kogo zrobiony rejestr"), max_length=30, null=True)

    def __str__(self):
        if self.points_log_type:
            return f"{self.points_log_class} - {self.points_log_date} + {self.points_log_amount} points."
        else:
            return f"{self.points_log_class} - {self.points_log_date} - {self.points_log_amount} points."
