from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, FormView
from .models import Stock, StockData, Feature
from .forms import StockDataForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

class StockListView(ListView):
    model = Stock
    template_name = 'stock_list.html'

class StockDetailView(DetailView):
    model = Stock
    template_name = 'stock_detail.html'

class AddStockDataView(FormView):
    template_name = 'add_stock_data.html'  # Template to render the form
    form_class = StockDataForm  # Form to use
    success_url = reverse_lazy('stock-list')  # Redirect URL after successful submission

    def form_valid(self, form):
        form.save()  # Save the form data to the database
        return super().form_valid(form)