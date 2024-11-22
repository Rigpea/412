from django.urls import path
from .views import StockListView, StockDetailView, AddStockDataView

urlpatterns = [
    path('', StockListView.as_view(), name='stock-list'),
    path('<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
     path('add/', AddStockDataView.as_view(), name='add-stock-data'),
]