from django.urls import path
from .views import HomeView, AddStockView, StocksAddedView, ChangeInvestmentView, evaluate_stock, action_completed, stock_details

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add/', AddStockView.as_view(), name='add_stocks'),
    path('stocks_added/', StocksAddedView.as_view(), name='stocks_added'),
    path('change/<int:pk>/', ChangeInvestmentView.as_view(), name='change_investment'),
    path('evaluate/<int:investment_id>/', evaluate_stock, name='evaluate_stock'),
    path('action_completed/', action_completed, name='action_completed'),
    path('stock/<int:stock_id>/', stock_details, name='stock_details'),


]