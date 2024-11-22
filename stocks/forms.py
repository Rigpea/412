from django import forms
from .models import StockData

class StockDataForm(forms.ModelForm):
    class Meta:
        model = StockData
        fields = ['stock', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']