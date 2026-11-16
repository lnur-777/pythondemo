# -*- coding: utf-8 -*-
"""
Application / Services Layer — Biznes Məntiqi və Maliyyə Hesablamaları (BudgetService).
"""

# ==============================================================================
# BLOK 1: İMPORTLAR, SİNFİN TƏYİNİ VƏ KONSTRUKTOR (__INIT__)
# ==============================================================================
from datetime import datetime
from domain.balance_summary import BalanceSummary
from domain.monthly_report_data import MonthlyReportData
from domain.transaction import Transaction
from interfaces.i_exchange_rate_provider import IExchangeRateProvider
from interfaces.i_transaction_repository import ITransactionRepository


class BudgetService:
    def __init__(self, repository: ITransactionRepository, rate_provider: IExchangeRateProvider) -> None:
        self._repository = repository
        self.exchange_rates = rate_provider.get_rates()
        self.transactions = self._repository.load_all()

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə "class BudgetService:" sətrində mötərizə YOXDUR, amma digər siniflərdə var idi?:
#    - Əgər sinif heç bir başqa sinifdən və ya interfeysdən miras ALMIRSA, mötərizə
#      yazılmır, birbaşa `class BudgetService:` yazılır!
#
# 2. "def __init__(self, repository: ITransactionRepository, rate_provider: IExchangeRateProvider) -> None:":
#    - `def`: Metod təyini açar sözü.
#    - `__init__`: Python-un standart konstruktor adı.
#    - `self`: C#-dakı `this` göstəricisi (konstruktorun və bütün adi metodların
#      1-ci parametri kimi məcburi yazılır).
#    - `self._repository = repository`: Obyektin içində `_repository` adlı private
#      dəyişən yaradır (qarşısındakı `_` işarəsi Python-da `private` deməkdir).
#    - `self.exchange_rates` və `self.transactions`: Qarşısında `_` olmadığı üçün
#      bunlar `public` property kimi digər siniflərdən oxuna bilir.
#
# C#-DA NECƏ YAZILIR?:
# public class BudgetService
# {
#     private readonly ITransactionRepository _repository;
#     public Dictionary<string, double> ExchangeRates { get; }
#     public List<Transaction> Transactions { get; }
#
#     public BudgetService(ITransactionRepository repository, IExchangeRateProvider rateProvider)
#     {
#         this._repository = repository;
#         this.ExchangeRates = rateProvider.GetRates();
#         this.Transactions = this._repository.LoadAll();
#     }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: VALYUTA ÇEVİRMƏ VƏ YENİ ƏMƏLİYYAT ƏLAVƏ ETMƏ METODLARI
# ==============================================================================
    def convert_to_azn(self, amount: float, currency: str) -> float:
        rate = self.exchange_rates.get(currency.upper(), 1.0)
        return round(amount * rate, 2)

    def add_transaction(
        self,
        transaction_type: str,
        amount: float,
        currency: str,
        category: str,
        description: str,
        date: str | None = None,
    ) -> Transaction:
        amount_azn = self.convert_to_azn(amount, currency)
        new_transaction = Transaction(
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            amount_azn=amount_azn,
            category=category,
            description=description,
            date=date or datetime.now().strftime("%Y-%m-%d"),
        )
        self.transactions.append(new_transaction)
        self._repository.save_all(self.transactions)
        return new_transaction

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "date: str | None = None" nə deməkdir?:
#    - `str | None` -> C#-dakı `string?` (nullable string).
#    - `= None`     -> C#-dakı `= null` (default dəyəri null-dur, yəni bu parametri
#      ötürməsəniz də olar).
#
# 2. "amount_azn = self.convert_to_azn(amount, currency)":
#    - Diqqət edin: `convert_to_azn` metodunun təyinində 3 parametr var idi:
#      `(self, amount, currency)`.
#    - Amma onu çağıranda `self.convert_to_azn(amount, currency)` kimi 2 arqument
#      ötürürük! Çünki nöqtədən əvvəlki `self` avtomatik 1-ci parametr kimi gedir.
#
# 3. "date or datetime.now().strftime('%Y-%m-%d')":
#    - C#-dakı `date ?? DateTime.Now.ToString("yyyy-MM-dd")` ifadəsidir.
#    - Əgər `date` dəyəri `None` (`null`) və ya boşdursa, `or` operatoru sağ tərəfdəki
#      bugünkü tarixi qaytarır.
#
# 4. "self.transactions.append(new_transaction)":
#    - C#-da siyahıya element əlavə etmək üçün `.Add(...)` yazılır, Python-da isə
#      `.append(...)` yazılır!
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: GENERATOR EXPRESSION (SUM) VƏ "ELIF / AND" SİNTAKSİSİ
# ==============================================================================
    def get_balance_summary(self) -> BalanceSummary:
        total_income = sum(tx.amount_azn for tx in self.transactions if tx.transaction_type == "gelir")
        total_expense = sum(tx.amount_azn for tx in self.transactions if tx.transaction_type == "xerc")
        net_balance = total_income - total_expense

        if net_balance < 0:
            status = "DİQQƏT! Xərcləriniz gəlirinizdən çoxdur (Kəsir var)."
        elif total_income > 0 and (net_balance / total_income) >= 0.20:
            status = "ƏLA! Gəlirinizin ən azı 20%-ni qənaət edə bilmisiniz."
        else:
            status = "NORMAL. Büdcəniz müsbətdir, lakin qənaəti artıra bilərsiniz."

        return BalanceSummary(total_income, total_expense, net_balance, status)

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "sum(tx.amount_azn for tx in self.transactions if tx.transaction_type == 'gelir')":
#    - Bu sətir 3 hissədən ibarətdir (C# LINQ ilə müqayisə):
#      * `for tx in self.transactions` -> `Transactions` siyahısını gəz
#      * `if tx.transaction_type == "gelir"` -> `.Where(tx => tx.TransactionType == "gelir")`
#      * `sum(tx.amount_azn ...)` -> `.Sum(tx => tx.AmountAzn)`
#
# 2. Niyə `status` dəyişənini `if`-dən əvvəl `string status;` kimi elan etmədik?:
#    - C#-da `if/else` içində dəyişənə dəyər mənimsədib sonra `return status;` etmək
#      üçün `if`-dən əvvəl `string status;` yazmalıyıq (yoxsa scope-da görünmür).
#    - Python-da isə `if / elif / else` blokları ayrı dəyişən scope-u YARATMIR!
#      `if` və ya `else` içində yaradılan `status` dəyişəni bütün metod boyu görünür.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 4: TUPLE QAYTARMAQ, LAMBDA VƏ SORTED SİNTAKSİSİ
# ==============================================================================
    def get_category_statistics(self) -> tuple[list[tuple[str, float, float]], float]:
        category_expenses: dict[str, float] = {}
        for tx in self.transactions:
            if tx.transaction_type == "xerc":
                category_expenses[tx.category] = category_expenses.get(tx.category, 0.0) + tx.amount_azn

        total_expense = sum(category_expenses.values())
        if total_expense == 0:
            return [], 0.0

        sorted_items = sorted(category_expenses.items(), key=lambda item: item[1], reverse=True)
        stats = [(cat, amt, (amt / total_expense) * 100) for cat, amt in sorted_items]
        return stats, total_expense

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "sorted(category_expenses.items(), key=lambda item: item[1], reverse=True)":
#    - `category_expenses.items()` lüğətdəki hər sətri `(açar, dəyər)` cütlüyü kimi verir:
#      `item[0]` -> kateqoriya adı (`Key`), `item[1]` -> xərc məbləği (`Value`).
#    - `key=lambda item: item[1]` -> C#-dakı `item => item.Value` lambda ifadəsidir!
#      Python-da `=>` oxu əvəzinə `lambda parametr: nəticə` yazılır.
#    - `reverse=True` -> Azalan sıra ilə (`OrderByDescending`).
#
# 2. "return [], 0.0" və "return stats, total_expense":
#    - Python-da `return` sözündən sonra vergüllə 2 dəyər yazdıqda, metod həmin
#      iki dəyəri avtomatik bir `tuple` (cütlük) kimi qaytarır!
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 5: FILTERING VƏ MAX(..., KEY=LAMBDA) SİNTAKSİSİ
# ==============================================================================
    def get_monthly_report(self, year_month: str) -> MonthlyReportData:
        monthly_txs = [tx for tx in self.transactions if tx.date.startswith(year_month)]
        monthly_income = sum(tx.amount_azn for tx in monthly_txs if tx.transaction_type == "gelir")
        expenses = [tx for tx in monthly_txs if tx.transaction_type == "xerc"]
        monthly_expense = sum(tx.amount_azn for tx in expenses)
        largest_expense = max(expenses, key=lambda tx: tx.amount_azn, default=None)
        return MonthlyReportData(year_month, monthly_txs, monthly_income, monthly_expense, largest_expense)

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "[tx for tx in self.transactions if tx.date.startswith(year_month)]":
#    - C# LINQ-dəki `Transactions.Where(tx => tx.Date.StartsWith(yearMonth)).ToList()`
#      sətrinin Python qarşılığıdır:
#      `[tx for tx in siyahı if şərt]`.
#
# 2. "max(expenses, key=lambda tx: tx.amount_azn, default=None)":
#    - `expenses` siyahısında `tx.amount_azn` dəyəri ən böyük olan obyekti tapır
#      (C# LINQ: `expenses.MaxBy(tx => tx.AmountAzn)` və ya `OrderByDescending(...).FirstOrDefault()`).
#    - `default=None`: Əgər `expenses` siyahısı boşdursa, xəta vermir və `None` (`null`) qaytarır.
# ------------------------------------------------------------------------------
