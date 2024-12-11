from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    # Fields to store fetched data
    latest_open = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latest_close = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latest_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latest_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100, default="My Portfolio")

    def __str__(self):
        return f"{self.name} - Owned by {self.user.name}"

    def company_count(self):

        return self.investments.values('stock').distinct().count()

class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='investments')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='investments')
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.stock.symbol} in {self.portfolio.name} - ${self.amount_invested}"
    
class TradeLog(models.Model):
    stock_symbol = models.CharField(max_length=10)
    action = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    quantity = models.IntegerField()
    order_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action.upper()} {self.quantity} of {self.stock_symbol} at {self.timestamp}"