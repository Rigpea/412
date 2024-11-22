from django.db import models

# Create your models here.
from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=100)  # Company name
    ticker = models.CharField(max_length=10, unique=True)  # Stock ticker symbol

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='data')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.stock.ticker} - {self.date}"


class Feature(models.Model):
    stock_data = models.ForeignKey(StockData, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=50)  # Feature name (e.g., RSI, Moving Average)
    value = models.FloatField()

    def __str__(self):
        return f"{self.name} for {self.stock_data.stock.ticker} on {self.stock_data.date}"