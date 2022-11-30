from collections import OrderedDict
from datetime import datetime

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(
        sorted(
            queryset.annotate(category_name=Coalesce("category__name", Value("-")))
            .order_by()
            .values("category_name")
            .annotate(s=Sum("amount"))
            .values_list("category_name", "s")
        )
    )


def total_per_year(queryset):
    years_months = set()
    for date in queryset.values_list("date", flat=True):
        years_months.add(
            (
                datetime.strptime(str(date), "%Y-%m-%d").year,
                datetime.strptime(str(date), "%Y-%m-%d").month,
            )
        )
    annual_expenses = {}
    for i in years_months:
        if str(i[0]) in annual_expenses.keys():
            annual_expenses[str(i[0])].update(
                {
                    str(i[1]): queryset.filter(
                        date__year=i[0], date__month=i[1]
                    ).aggregate(Sum("amount"))
                }
            )
        else:
            annual_expenses[str(i[0])] = {
                str(i[1]): queryset.filter(date__year=i[0], date__month=i[1]).aggregate(
                    Sum("amount")
                )
            }
    return annual_expenses
