from django.views.generic import TemplateView, FormView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from .models import User, Portfolio, Investment, Stock
from .forms import StockForm
from .forms import ChangeInvestmentForm
from .utils import fetch_stock_data, moving_average_strategy, execute_trade
from django.http import HttpResponse
import alpaca_trade_api as tradeapi
from django.conf import settings
from .utils import fetch_stock_data


def action_completed(request):
    """
    Render a simple action completed page.
    """
    return render(request, 'stocks/action_completed.html')

from django.shortcuts import get_object_or_404, redirect
from .utils import fetch_stock_data, moving_average_strategy, execute_trade
from .models import Investment

def evaluate_stock(request, investment_id):
    """
    Manually evaluate a stock and decide to buy or sell based on strategy.
    """
    # Get the investment record
    investment = get_object_or_404(Investment, id=investment_id)

    # Fetch stock data
    try:
        data = fetch_stock_data(investment.stock.symbol, "2024-01-01", "2024-12-31")
    except Exception as e:
        return redirect('action_completed')  


    data = moving_average_strategy(data)
    last_signal = data.iloc[-1]['signal']
    api = tradeapi.REST(
        settings.ALPACA_API_KEY,
        settings.ALPACA_SECRET_KEY,
        settings.ALPACA_BASE_URL,
        api_version="v2"
    )


    try:
        if last_signal == 1:
            execute_trade(api, investment.stock.symbol, "buy", 10)  # Buy 10 stocks
        elif last_signal == -1:
            execute_trade(api, investment.stock.symbol, "sell", 10)  # Sell 10 stocks

        return redirect('action_completed')
    except Exception as e:
        return redirect('action_completed')  
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.first()
        if not user:
            context['user'] = None
            context['investments'] = None
            return context

        portfolio = user.portfolios.first()
        if not portfolio:
            portfolio = Portfolio.objects.create(user=user, name="My Portfolio")

        investments = portfolio.investments.select_related('stock')
        context['user'] = user
        context['investments'] = investments
        return context


class AddStockView(FormView):
    template_name = "stocks/add_stocks.html"
    form_class = StockForm
    success_url = reverse_lazy('stocks_added')

    def form_valid(self, form):
        # Save the stock
        stock = form.save()

        # Fetch stock data
        try:
            data = fetch_stock_data(stock.symbol, "2024-01-01", "2024-12-31")  

            stock.latest_open = data.iloc[-1]['open']
            stock.latest_close = data.iloc[-1]['close']
            stock.latest_high = data.iloc[-1]['high']
            stock.latest_low = data.iloc[-1]['low']
            stock.save()
        except Exception as e:
            # Log the error or handle it (optional)
            print(f"Error fetching stock data: {e}")

        # Get the user's portfolio
        user = User.objects.first() 
        portfolio = user.portfolios.first()

        # Create an investment in the portfolio
        Investment.objects.create(
            portfolio=portfolio,
            stock=stock,
            amount_invested=form.cleaned_data['amount_invested']
        )
        return super().form_valid(form)


class StocksAddedView(TemplateView):
    template_name = "stocks/stocks_added.html"

class ChangeInvestmentView(FormView):
    template_name = "stocks/change_investment.html"
    form_class = ChangeInvestmentForm

    def get_object(self):
        investment_id = self.kwargs['pk']
        return get_object_or_404(Investment, pk=investment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment'] = self.get_object()
        return context

    def form_valid(self, form):
        investment = self.get_object()

        # Handle addition to investment amount
        if form.cleaned_data['add_amount']:
            investment.amount_invested += form.cleaned_data['add_amount']
            investment.save()

        # Handle deletion
        if form.cleaned_data['delete']:
            investment.delete()
            return redirect(reverse_lazy('home'))  # Redirect to home after deletion

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('change_investment', kwargs={'pk': self.get_object().pk})


def stock_details(request, stock_id):
    """
    Fetch and display details of a stock using the Alpaca API.
    """
    # Get the stock object
    stock = get_object_or_404(Stock, id=stock_id)

    # Fetch stock data from Alpaca
    try:
        data = fetch_stock_data(stock.symbol, "2024-01-01", "2024-01-31")  # Example date range
        # Convert DataFrame to a list of dictionaries
        data_records = data.reset_index().to_dict(orient='records')
    except Exception as e:
        return render(request, 'stocks/stock_details.html', {
            'stock': stock,
            'error': f"Error fetching data: {e}"
        })

    # Render the template with the stock data
    return render(request, 'stocks/stock_details.html', {
        'stock': stock,
        'data': data_records
    })

    # Render the template with the stock data
    return render(request, 'stocks/stock_details.html', {
        'stock': stock,
        'data': data
    })