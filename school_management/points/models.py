from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone


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
        ("Klasy początkowe", "Klasy początkowe"),
        ("Klasy średnie", "Klasy średnie"),
        ("Klasy starsze", "Klasy starsze"),
    ]

    class_number = models.PositiveSmallIntegerField(verbose_name="Numer klasy",
        validators=[MinValueValidator(1), MaxValueValidator(12)], null=False
    )
    class_letter = models.CharField(verbose_name="Litera klasy",
        max_length=1, choices=SCHOOL_LETTER_CHOICES, default="A"
    )
    class_school_level = models.CharField("Poziom szkolnictwa",
        max_length=16, choices=SCHOOL_LEVEL_CHOICES, default="Klasy średnie"
    )
    class_teacher_name = models.CharField(verbose_name="Imię wychowawczyni", max_length=20)
    class_teacher_surname = models.CharField(verbose_name="Nazwisko wychowawczyni", max_length=20)
    class_points = models.PositiveSmallIntegerField(verbose_name="Punkty",
        validators=[MinValueValidator(0), MaxValueValidator(999)], null=False,
        default=0
    )

    def __str__(self):
        return f"{self.class_number}{str(self.class_letter).capitalize()} - {self.class_school_level}"


class Article(models.Model):
    title = models.CharField(verbose_name="Nazwa tytułowa", max_length=50)
    cover_photo = models.ImageField(verbose_name="Zdjęcie główne")
    description = models.TextField(verbose_name="Opis")
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PointsLog(models.Model):
    points_log_class = models.ForeignKey(Classes, verbose_name="Klasa rejestru", on_delete=models.CASCADE, null=True)
    points_log_date = models.DateField(verbose_name="Data rejestru", auto_now_add=True)
    points_log_type = models.BooleanField(verbose_name="Typ rejestru", null=True, blank=True)
    points_log_amount = models.PositiveSmallIntegerField(verbose_name="Ilość punktów",
        validators=[MinValueValidator(1), MaxValueValidator(100)], null=False
    )
    points_log_created_by = models.CharField(verbose_name="Przez kogo zorbiony rejestr", max_length=30, null=True)

    def __str__(self):
        if self.points_log_type:
            return f"{self.points_log_class} - {self.points_log_date} - ADDED {self.points_log_amount} points."
        else:
            return f"{self.points_log_class} - {self.points_log_date} - SUBTRACTED {self.points_log_amount} points."
