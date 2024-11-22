from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Stock, StockData, Feature

admin.site.register(Stock)
admin.site.register(StockData)
admin.site.register(Feature)