from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    date_from = forms.DateField()
    date_to = forms.DateField()
    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Category.objects.values_list("name", "name"),
    )

    class Meta:
        model = Expense
        fields = ["name", "date", "date_from", "date_to", "categories"]

    def __init__(self, *args, **kwargs):
        super(ExpenseSearchForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["date"].required = False
        self.fields["date_from"].required = False
        self.fields["date_to"].required = False
        self.fields["categories"].required = False
