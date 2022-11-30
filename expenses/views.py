from django.views.generic.list import ListView
from django.db.models import Sum

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_per_year


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        sorted_by = self.request.GET.get("order_by")
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name", "").strip()
            date = form.cleaned_data.get("date")
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            category = form.cleaned_data.get("categories")

            if name:
                queryset = queryset.filter(name__icontains=name)
            if date:
                queryset = queryset.filter(date__icontains=date)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
            if date_from and date_to:
                queryset = queryset.filter(date__gte=date_from, date__lte=date_to)
            if category:
                queryset = queryset.filter(category__name__in=category)
            if sorted_by:
                queryset = queryset.order_by(sorted_by)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            amount_sum=queryset.aggregate(Sum("amount")),
            summary_per_category=summary_per_category(queryset),
            annual_expenses=total_per_year(queryset),
            **kwargs
        )


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        expenses_amount = []
        for item in queryset.values():
            item["amount"] = Expense.objects.filter(category=item["id"]).count()
            expenses_amount.append(item)

        return super().get_context_data(expenses_amount=expenses_amount, **kwargs)
