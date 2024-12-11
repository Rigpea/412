from django import forms
from .models import Stock
from .models import Investment

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'symbol']
    
    amount_invested = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount to Invest",
        required=True,
    )

from django import forms
from .models import Investment

class ChangeInvestmentForm(forms.ModelForm):
    add_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Add to Investment Amount",
        help_text="Enter an amount to add to the current investment."
    )
    delete = forms.BooleanField(
        required=False,
        label="Delete Stock",
        help_text="Check this box to delete the stock."
    )

    class Meta:
        model = Investment
        fields = []  # No direct model fields are updated via the form