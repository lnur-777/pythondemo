# -*- coding: utf-8 -*-
"""
Infrastructure Layer — JSON Fayl əsaslı Əməliyyat Repository-si (JsonTransactionRepository).
"""

# ==============================================================================
# BLOK 1: KİTABXANALARIN İMPORTU VƏ KONSTRUKTOR
# ==============================================================================
import json
import os
from domain.transaction import Transaction
from interfaces.i_transaction_repository import ITransactionRepository


class JsonTransactionRepository(ITransactionRepository):
    def __init__(self, file_name: str = "budce_melumatlari.json") -> None:
        self.file_name = file_name

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
# - `class JsonTransactionRepository(ITransactionRepository):`:
#   Mötərizə içində yazılan `ITransactionRepository` bu sinfin həmin interfeysdən
#   miras aldığını (C#-dakı `: ITransactionRepository`) bildirir.
# - `def __init__(self, file_name: str = "budce_melumatlari.json") -> None:`:
#   Sinfin konstruktorudur. `self.file_name = file_name` ilə obyektin daxilində
#   `file_name` adlı dəyişən (field) yaradılır.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: FAYLDAN OXUMA VƏ LIST COMPREHENSION ([... FOR ... IN ...]) SİNTAKSİSİ
# ==============================================================================
    def load_all(self) -> list[Transaction]:
        if not os.path.exists(self.file_name):
            return []

        try:
            with open(self.file_name, mode="r", encoding="utf-8") as json_file:
                data_list = json.load(json_file)
                transactions = [Transaction.from_dict(item) for item in data_list]
            print(f"[Sistem] Bazadan {len(transactions)} əməliyyat uğurla yükləndi.")
            return transactions
        except (json.JSONDecodeError, KeyError, IOError) as error:
            print(f"[Xəta] Fayl oxunarkən problem yarandı: {error}. Yeni baza yaradılacaq.")
            return []

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "return []" nədir?:
#    - Python-da boş kvadrat mötərizə `[]` yeni boş siyahı (`new List<Transaction>()`)
#      yaratmaq deməkdir!
#
# 2. "with open(self.file_name, mode='r', encoding='utf-8') as json_file:":
#    - `open(...)` faylı açır (`mode="r"` = read/oxumaq).
#    - `with ... as json_file:` C#-dakı `using (var jsonFile = File.OpenText(...))`
#      blokudur. Abzasla sağa çəkilmiş 2 sətir bitən kimi Python faylı avtomatik bağlayır!
#
# 3. "[Transaction.from_dict(item) for item in data_list]" necə oxunur?:
#    - Buna Python-da **List Comprehension** deyilir və C#-dakı **LINQ `.Select(...).ToList()`**
#      ifadəsinin tək sətirlik qarşılığıdır.
#    - Kvadrat mötərizə `[ ... ]` nəticənin yeni bir `list` olacağını göstərir.
#    - Sağ tərəfdəki `for item in data_list` dövrü `data_list`-dəki hər elementi
#      növbə ilə `item` dəyişəninə götürür, sol tərəfdəki `Transaction.from_dict(item)`
#      isə onu `Transaction` obyektinə çevirib yeni siyahıya əlavə edir.
#    - Əgər bunu adi `for` ilə yazsaydıq, 4 sətir olacaqdı:
#          transactions = []
#          for item in data_list:
#              transactions.append(Transaction.from_dict(item))
#
# C#-DA NECƏ YAZILIR?:
# public List<Transaction> LoadAll()
# {
#     if (!File.Exists(_fileName))
#         return new List<Transaction>();
#     ...
#     var transactions = dataList.Select(item => Transaction.FromDict(item)).ToList();
#     return transactions;
# }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: FAYLA YAZMA SİNTAKSİSİ (SAVE_ALL)
# ==============================================================================
    def save_all(self, transactions: list[Transaction]) -> None:
        try:
            dict_list = [tx.to_dict() for tx in transactions]
            with open(self.file_name, mode="w", encoding="utf-8") as json_file:
                json.dump(dict_list, json_file, ensure_ascii=False, indent=4)
        except IOError as error:
            print(f"[Xəta] Məlumatlar fayla yazıla bilmədi: {error}")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "dict_list = [tx.to_dict() for tx in transactions]":
#    - Yenə List Comprehension: `transactions` siyahısındakı hər bir `tx` obyektinin
#      `tx.to_dict()` metodunu çağırır və alınan lüğətlərdən yeni siyahı düzəldir
#      (C#-da: `transactions.Select(tx => tx.ToDict()).ToList()`).
#
# 2. "json.dump(dict_list, json_file, ensure_ascii=False, indent=4)":
#    - `False` böyük `F` hərfi ilə yazılır (C#-da `false`).
#    - `ensure_ascii=False` və `indent=4` adlandırılmış arqumentlərdir (C#-dakı
#      `ensureAscii: false, indent: 4`).
# ------------------------------------------------------------------------------
