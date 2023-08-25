import django_filters
from .models import PointsLog
from django.utils.translation import gettext_lazy as _


class PointsLogFilter(django_filters.FilterSet):
    log_create_date_year = django_filters.NumberFilter(label=_("Rok rejestru(-ów)"),
        field_name="points_log_date", lookup_expr="year"
    )
    log_create_date_month = django_filters.NumberFilter(label=_("Mesiąc rejestru(-ów)"),
        field_name="points_log_date", lookup_expr="month"
    )
    log_create_date_day = django_filters.NumberFilter(label=_("Dzień rejestru(-ów)"),
        field_name="points_log_date", lookup_expr="day"
    )

    class Meta:
        model = PointsLog
        fields = ["points_log_class"]
        labels = {
            "points_log_class": "Klasa rejestru(-ów)",
        }
