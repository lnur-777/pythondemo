# -*- coding: utf-8 -*-
"""
Domain Layer — Transaction (Əməliyyat) Entity / Model sinfi.
"""

# ==============================================================================
# BLOK 1: KİTABXANALARIN İMPORT EDİLMƏSİ
# ==============================================================================
from dataclasses import dataclass, field
from datetime import datetime

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
# - Python-da "from X import Y, Z" sintaksisi "X" kitabxanasının içindən yalnız
#   "Y" və "Z" elementlərini gətirir.
# - "dataclasses" Python-un standart kitabxanasıdır: model sinifləri yaratmağı
#   C#-dakı "record" və ya "{ get; set; }" auto-property-lər kimi asanlaşdırır.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: @DATACLASS VƏ PROPERTY-LƏRİN TƏYİNİ
# ==============================================================================
@dataclass
class Transaction:
    transaction_type: str
    amount: float
    currency: str
    amount_azn: float
    category: str
    description: str = ""
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "@dataclass" nədir? ("@" işarəsi nə deməkdir?):
#    - Python-da "@" işarəsi ilə başlayan ifadələrə "Decorator" deyilir. C#-dakı
#      "[Serializable]" və ya "[JsonPropertyName]" kimi atributların (`[Attribute]`)
#      qarşılığıdır.
#    - Normalda Python sinfində bütün dəyişənləri "def __init__(self, ...):" içində
#      tək-tək "self.amount = amount" kimi yazmaq lazımdır.
#    - Sinfin üzərinə "@dataclass" yazdıqda isə Python C#-dakı "record" kimi həmin
#      "__init__" konstruktorunu arxa planda bizim əvəzimizə АВТОМАТİK yaradır!
#
# 2. "transaction_type: str" və "amount: float" necə oxunur?:
#    - C#-da: `public string TransactionType { get; set; }` (əvvəl tip, sonra ad).
#    - Python-da: `transaction_type: str` (əvvəl ad, sonra `:` işarəsi, sonra tip).
#    - Python-da `str` = C# `string`, `float` = C# `double`, `int` = C# `int`, `bool` = C# `bool`.
#    - `description: str = ""` -> susmaya görə (default) dəyəri boş sətirdir.
#
# 3. "field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))":
#    - "lambda:" C#-dakı `() => ...` (ox funksiyası / anonim funksiya) deməkdir!
#    - Yəni C#-da `() => DateTime.Now.ToString("yyyy-MM-dd")` necə yazılırsa,
#      Python-da `lambda: datetime.now().strftime("%Y-%m-%d")` elə yazılır.
#    - Niyə `default_factory` istifadə olunub? Hər dəfə yeni `Transaction` obyekti
#      yaradılanda həmin anın tarixini dinamik hesablasın deyə.
#
# C#-DA NECƏ YAZILIR?:
# public class Transaction
# {
#     public string TransactionType { get; set; }
#     public double Amount { get; set; }
#     public string Currency { get; set; }
#     public double AmountAzn { get; set; }
#     public string Category { get; set; }
#     public string Description { get; set; } = "";
#     public string Date { get; set; } = DateTime.Now.ToString("yyyy-MM-dd");
# }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: __POST_INIT__ METODU (KONSTRUKTORDAN DƏRHAL SONRA İŞLƏYƏN METOD)
# ==============================================================================
    def __post_init__(self) -> None:
        self.amount = float(self.amount)
        self.currency = self.currency.upper()
        self.amount_azn = float(self.amount_azn)
        self.category = self.category.strip().capitalize()
        self.description = self.description.strip()
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə "__init__" yox, "__post_init__" yazılıb?:
#    - Yuxarıda "@dataclass" yazdığımız üçün "__init__" konstruktorunu Python özü
#      avtomatik yaradıb (dəyərləri `self.amount`, `self.currency` və s. içərisinə qoyub).
#    - Əgər biz konstruktor dəyərləri mənimsətdikdən DƏRHAL SONRA əlavə yoxlama və ya
#      formatlama etmək istəyiriksə, "@dataclass" bizə xüsusi "__post_init__(self)"
#      metodunu təqdim edir. Obyekt yaranan kimi avtomatik işə düşür!
#
# 2. "float(self.amount)" nədir?:
#    - C#-dakı `(double)amount` və ya `Convert.ToDouble(amount)` tip çevirməsidir (Casting).
#
# 3. String metodları (.NET qarşılıqları):
#    - `.upper()`      -> C#-da `.ToUpper()`
#    - `.strip()`      -> C#-da `.Trim()` (əvvəldəki və sondakı boşluqları silir)
#    - `.capitalize()` -> C#-da birbaşa tək metod yoxdur; sözün ilk hərfini böyük,
#                         qalan hərflərini kiçik edir (məs: "qİDA" -> "Qida").
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 4: TO_DICT METODU (PYTHON DICTIONARY / LÜĞƏT SİNTAKSİSİ)
# ==============================================================================
    def to_dict(self) -> dict:
        return {
            "nov": self.transaction_type,
            "mebleg": self.amount,
            "valyuta": self.currency,
            "mebleg_azn": self.amount_azn,
            "kateqoriya": self.category,
            "aciqlama": self.description,
            "tarix": self.date,
        }

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Bəs bayaq dedik Python-da "{ }" yoxdur, buradakı "{ ... }" nədir?:
#    - Çox vacib fərq: Python-da "{ }" blok (metod/if/for) açmaq üçün İSTİFADƏ OLUNMUR!
#    - Python-da "{ }" yalnız "dict" (C#-dakı `Dictionary<TKey, TValue>`) yaratmaq üçün
#      istifadə olunur!
#    - Yəni `return { "nov": self.transaction_type, ... }` yazılışı C#-dakı
#      `return new Dictionary<string, object> { ["nov"] = this.TransactionType, ... };`
#      deməkdir.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 5: @CLASSMETHOD VƏ FROM_DICT METODU ("CLS" VS "SELF" FƏRQİ)
# ==============================================================================
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            transaction_type=data["nov"],
            amount=data["mebleg"],
            currency=data["valyuta"],
            amount_azn=data["mebleg_azn"],
            category=data["kateqoriya"],
            description=data.get("aciqlama", ""),
            date=data["tarix"],
        )

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə burada "self" yox, "@classmethod" və "cls" yazılıb?:
#    - Adi metodlarda ("def to_dict(self):") əlimizdə artıq hazır obyekt var və
#      "self" həmin obyekti (`this`) göstərir.
#    - Amma "from_dict" çağırılanda əlimizdə hələ `Transaction` obyekti YOXDUR! Biz
#      JSON-dan gələn `data` lüğətindən YENİ bir `Transaction` obyekti yaratmaq istəyirik
#      (C#-dakı `public static Transaction FromDict(...)`).
#    - Python-da metodun üzərinə `@classmethod` yazdıqda, birinci parametr obyekt (`self`)
#      deyil, sinfin özü (`cls` = `Transaction` sinfi) olur.
#    - İçəridə `return cls(...)` yazmaq elə `return Transaction(...)` (C#-da
#      `return new Transaction(...)`) deməkdir!
#
# 2. Niyə `-> "Transaction"` dırnaq içində yazılıb?:
#    - Çünki biz hələ `class Transaction:` blokunun içindəyik, sinfin təyini tam
#      bitməyib. Python-da sinfin öz içində öz adını tip kimi göstərəndə dırnaq
#      içində `"Transaction"` yazmaq (Forward Reference) qəbul olunmuş üsuldur.
#
# 3. `data["nov"]` vs `data.get("aciqlama", "")` fərqi nədir?:
#    - `data["nov"]`: C#-dakı `data["nov"]` kimidir — əgər lüğətdə `"nov"` açarı
#      yoxdursa, proqram `KeyError` (C#-da `KeyNotFoundException`) atır.
#    - `data.get("aciqlama", "")`: C#-dakı `data.GetValueOrDefault("aciqlama", "")`
#      kimidir — açar tapılmasa xəta atmır, ikinci arqumentdəki `""` dəyərini qaytarır.
# ------------------------------------------------------------------------------
