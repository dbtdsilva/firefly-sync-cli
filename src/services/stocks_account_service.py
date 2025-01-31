
import logging
import re
from typing import Dict, List, Tuple

from ..firefly_api.models.transaction_type import TransactionType

from ..firefly_api.models.transaction import Transaction
from .base_service import BaseService
from ..firefly_api.api import FireflyApi
from ..firefly_api.models.account_type import AccountType
from ..firefly_api.models.account import Account
from datetime import datetime, timedelta
import yfinance as yf
import pytz


class StocksAccountService(BaseService):

    def __init__(self, api: FireflyApi, dry_run: bool) -> None:
        super().__init__(api, dry_run)

    def update_all(self) -> None:
        for account, movements in self.__find_accounts_matching_stocks():
            self.__update_account(account, movements)

    def __update_account(self, account: Account, movements: List[Tuple[datetime, str, float]]):
        transactions = self.api.accounts.get_account_transactions(account_id=account.id)
        if len(transactions) == 0:
            no_transaction_date = self.__find_first_movement_date(movements)
            previous_value = 0
        else:
            transaction = self.__find_last_transaction(transactions)
            no_transaction_date = transaction.date.replace(tzinfo=None) + timedelta(days=1)
            previous_value = float(transaction.internal_reference)

        now = datetime.now()
        transaction_date = no_transaction_date.replace(hour=23, minute=59, second=0, microsecond=0)
        while transaction_date < now:
            portfolio = self.__get_portfolio_at(transaction_date, movements)
            transaction = self.__create_transaction(account, transaction_date, portfolio, previous_value)

            if abs(transaction.amount) > 0.0001:
                if not self.dry_run:
                    self.api.transactions.store_transaction(transaction)
                logging.info(f'Finished updating stocks for account {account.name} at {transaction_date} with '
                             f'{len(portfolio)} different stocks')
            previous_value = float(transaction.internal_reference)
            transaction_date += timedelta(days=1)

    def __create_transaction(self, account: Account, date: datetime, portfolio: List[Tuple[str, float]],
                             previous_value) -> Transaction:
        rates_per_stock = self.__get_market_rate_portfolio(date, account.currency_code, portfolio)
        portfolio_value = self.__get_portfolio_value_at(rates_per_stock, portfolio)
        value = portfolio_value - previous_value
        default_unknown_account = "Unidentified"
        if value >= 0:
            transaction_type = TransactionType.DEPOSIT
            source_name = default_unknown_account
            destination_name = account.name
        else:
            transaction_type = TransactionType.WITHDRAWAL
            source_name = account.name
            destination_name = default_unknown_account

        currency_code = account.currency_code
        notes = '\n\n'.join([f"**{stock}**: {quantity} x {rates_per_stock[stock]}" for stock, quantity in portfolio])

        return Transaction(
            source_name=source_name,
            destination_name=destination_name,
            description='Automatic stock value daily update',
            amount=abs(value),
            date=date,
            currency_code=currency_code,
            internal_reference=str(float(portfolio_value)),
            type=transaction_type,
            notes=notes,
            tags=['stock'])

    def __get_market_rate_portfolio(self, dt: datetime, currency: str, portfolio: List[Tuple[str, float]]) -> Dict[str, float]:
        rate_per_stock = {}
        for stock, _ in portfolio:
            rate_per_stock[stock] = self.__get_market_rate_at(dt, stock, currency)
        return rate_per_stock

    def __get_portfolio_value_at(self, rate_per_stock: Dict[str, float], portfolio: List[Tuple[str, float]]) -> float:
        value = 0
        for stock, quantity in portfolio:
            value += rate_per_stock[stock] * quantity
        return value

    def __get_portfolio_at(self, dt: datetime, movements: List[Tuple[datetime, str, float]]) -> List[Tuple[str, float]]:
        stock_quantities = {}
        for movement_dt, stock, quantity in movements:
            if movement_dt > dt:
                continue

            if stock in stock_quantities:
                stock_quantities[stock] += quantity
            else:
                stock_quantities[stock] = quantity

            if stock_quantities[stock] == 0:
                stock_quantities.pop(stock)
        return list(stock_quantities.items())

    def __find_last_transaction(self, transactions: List[Transaction]) -> Transaction:
        return max(transactions, key=lambda t: t.date)

    def __find_first_movement_date(self, movements: Tuple[datetime, str, float]) -> datetime:
        return min(movements, key=lambda x: x[0])[0]

    def __find_accounts_matching_stocks(self) -> List[Tuple[Account, List[Tuple[datetime, str, float]]]]:
        accounts = self.api.accounts.get_accounts(AccountType.ASSET)
        stock_accounts = []
        for account in accounts:
            stock_movements = []
            for line in account.notes.split('\n'):
                pattern = r"sync_stock:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\s*([^,:;]+),\s*(-?\d+(?:\.\d+)?)"
                parsed = re.search(pattern, line, re.MULTILINE)
                if not parsed or len(parsed.groups()) != 3:
                    logging.warning(f'Skipping account match, no notes with sync for stocks: {account.name}')
                    continue

                timestamp, ticker, value = parsed.groups()
                stock_movements.append((datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"), ticker, float(value)))
            if len(stock_movements) != 0:
                stock_accounts.append((account, stock_movements))
        return stock_accounts

    def __get_market_rate_at(self, date: datetime, label: str, currency: str) -> float:
        if label.startswith('CASH_'):
            return self.__get_exchange_rate(label.replace('CASH_', ''), currency, date)
        return self.__get_stock_price(date, label, currency)

    def __get_stock_price(self, date: datetime, ticker: str, currency: str) -> float:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        exchange_tz = stock_info.get('exchangeTimezoneName', 'UTC')
        tz = pytz.timezone(exchange_tz)
        localized_date = tz.localize(date)
        start_date = localized_date - timedelta(days=7)
        end_date = localized_date + timedelta(days=1)

        stock_currency = stock_info.get("currency")
        if stock_currency is None:
            raise ValueError(f"Failed to retrieve currency for {ticker}")

        data = stock.history(start=start_date.strftime('%Y-%m-%d'),
                             end=end_date.strftime('%Y-%m-%d'),
                             interval="1d")
        if data.empty:
            raise ValueError(f"No data found for {ticker} around {localized_date.date()}")

        # Localize the data index to the exchange's timezone
        data.index = data.index.tz_convert(tz)

        # Filter data to include only entries up to the target date
        valid_data = data[data.index <= localized_date]
        if valid_data.empty:
            raise ValueError(f"No data found for {ticker} on or before {localized_date.date()}")

        closing_price = float(valid_data["Close"].iloc[-1])
        closing_datetime = valid_data.index.max()
        return closing_price * self.__get_exchange_rate(stock_currency, currency, closing_datetime)

    def __get_exchange_rate(self, source_currency: str, destination_currency: str, date: datetime):
        if source_currency == destination_currency:
            return 1

        fx_ticker = f"{source_currency}{destination_currency}=X"  # Example: 'EURUSD=X' for USD to EUR
        fx_data = yf.Ticker(fx_ticker).history(start=date, end=date, interval="1d")
        if fx_data.empty:
            raise ValueError(f"No exchange rate found for {source_currency} to {destination_currency} on {date}")
        exchange_rate = float(fx_data["Close"].iloc[0])
        return exchange_rate
