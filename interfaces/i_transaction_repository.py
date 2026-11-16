# -*- coding: utf-8 -*-
"""
Interfaces Layer — Əməliyyat Bazası İnterfeysi (ITransactionRepository).
"""

# ==============================================================================
# BLOK 1: REPOSITORY İNTERFEYSİ VƏ METOD İMZALARI
# ==============================================================================
from abc import ABC, abstractmethod
from domain.transaction import Transaction


class ITransactionRepository(ABC):
    @abstractmethod
    def load_all(self) -> list[Transaction]:
        pass

    @abstractmethod
    def save_all(self, transactions: list[Transaction]) -> None:
        pass

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "class ITransactionRepository(ABC):":
#    - C#-dakı `public interface ITransactionRepository` qarşılığıdır.
#    - Mötərizədə `(ABC)` yazmaq bu sinfin abstrakt (interfeys) olduğunu göstərir.
#    - Sonda qoyulan `:` işarəsi C#-da sinfin açılan `{` mötərizəsidir.
#
# 2. "def load_all(self) -> list[Transaction]:":
#    - `def`: Metod təyini açar sözü.
#    - `self`: İnterfeys metodlarında da birinci parametr həmişə `self` yazılır.
#    - `-> list[Transaction]`: Metodun geri qaytaracağı tip (C#-da `List<Transaction>`).
#
# 3. "def save_all(self, transactions: list[Transaction]) -> None:":
#    - `transactions: list[Transaction]`: Parametrin adı `transactions`, tipi isə
#      `list[Transaction]`-dır (C#-da tərsinə yazılır: `List<Transaction> transactions`).
#    - `-> None`: Metod heç bir dəyər qaytarmır (C#-dakı `void`).
#
# 4. Niyə hər iki metodun içində "pass" yazılıb və bir metodun bitib digərinin
#    başladığı necə bilinir?:
#    - `def load_all...:` sətrindən sonra 8 boşluq içəridə yazılan `pass` həmin
#      metodun gövdəsidir (C#-da interfeys metodunun sonundakı `;` əvəzi).
#    - Növbəti `@abstractmethod` və `def save_all...:` yenidən 4 boşluğa (sola)
#      qayıtdığı üçün Python bilir ki, `load_all` metodu artıq bitib!
#
# C#-DA NECƏ YAZILIR?:
# public interface ITransactionRepository
# {
#     List<Transaction> LoadAll();
#     void SaveAll(List<Transaction> transactions);
# }
# ------------------------------------------------------------------------------
