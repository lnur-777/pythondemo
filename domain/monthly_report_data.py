# -*- coding: utf-8 -*-
"""
Domain Layer — MonthlyReportData (Aylıq Hesabat Məlumatları) DTO / Model sinfi.
"""

# ==============================================================================
# BLOK 1: GENERIC LIST VƏ NULLABLE ("| None") TİP SİNTAKSİSİ
# ==============================================================================
from dataclasses import dataclass
from domain.transaction import Transaction


@dataclass
class MonthlyReportData:
    year_month: str
    transactions: list[Transaction]
    monthly_income: float
    monthly_expense: float
    largest_expense: Transaction | None

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "transactions: list[Transaction]" nədir? (Niyə "< >" yox, "[ ]" yazılıb?):
#    - C#-da Generic tiplər bucaq mötərizəsi ilə yazılır: `List<Transaction>`.
#    - Python-da isə Generic tiplər kvadrat mötərizə `[ ]` ilə yazılır: `list[Transaction]`!
#    - Eyni qayda lüğətlər üçün də keçərlidir: C#-da `Dictionary<string, double>`,
#      Python-da isə `dict[str, float]`.
#
# 2. "largest_expense: Transaction | None" nədir? ("|" işarəsi nə deməkdir?):
#    - C#-da bir dəyişənin "null" ola biləcəyini göstərmək üçün sual işarəsi qoyuruq:
#      `Transaction? LargestExpense`.
#    - Python-da "null" sözünün qarşılığı "None"-dır.
#    - "|" işarəsi "VƏ YA" (Union Type) deməkdir: yəni `largest_expense` dəyişəninin
#      içində ya `Transaction` obyekti olacaq, ya da `None` (`null`) olacaq!
#
# C#-DA NECƏ YAZILIR?:
# public record MonthlyReportData(
#     string YearMonth,
#     List<Transaction> Transactions,
#     double MonthlyIncome,
#     double MonthlyExpense,
#     Transaction? LargestExpense
# );
# ------------------------------------------------------------------------------
