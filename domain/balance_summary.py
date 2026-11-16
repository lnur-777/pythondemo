# -*- coding: utf-8 -*-
"""
Domain Layer — BalanceSummary (Balans Hesabatı) DTO / Model sinfi.
"""

# ==============================================================================
# BLOK 1: @DATACLASS İLƏ MODEL SİNFİNİN TƏYİNİ
# ==============================================================================
from dataclasses import dataclass


@dataclass
class BalanceSummary:
    total_income: float
    total_expense: float
    net_balance: float
    status_message: str

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə bu sinifdə "def __init__(self, ...)" YOXDUR?:
#    - Əgər sinfin üzərinə "@dataclass" yazmasaydıq, məcbur idik belə yazaq:
#          class BalanceSummary:
#              def __init__(self, total_income: float, total_expense: float, ...):
#                  self.total_income = total_income
#                  self.total_expense = total_expense
#                  ...
#    - "@dataclass" dekoratoru bizi bu təkrarçılıqdan xilas edir: yuxarıdakı 4 sətri
#      görüb arxa planda həmin "__init__" konstruktorunu özü avtomatik yaradır!
#    - C#-dakı "public record BalanceSummary(double TotalIncome, ...);" sintaksisinin
#      Python-dakı birbaşa qarşılığı məhz "@dataclass"-dır.
#
# 2. Sinfin içi harada başlayır və harada bitir?:
#    - "class BalanceSummary:" sətrinin sonundakı ":" işarəsi C#-dakı "{" deməkdir.
#    - Ondan aşağıda 4 boşluq (1 Tab) sağa sürüşdürülmüş 4 sətir sinfin içindədir.
#      Fayl bitdiyi (və ya abzas sola qayıtdığı) anda sinif də bitir (C#-dakı "}").
#
# C#-DA NECƏ YAZILIR?:
# public record BalanceSummary(
#     double TotalIncome,
#     double TotalExpense,
#     double NetBalance,
#     string StatusMessage
# );
# ------------------------------------------------------------------------------
