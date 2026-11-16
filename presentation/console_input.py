# -*- coding: utf-8 -*-
"""
Presentation Layer — Konsol Girişi və İstifadəçi Məlumatlarının Yoxlanması (ConsoleInput).
"""

# ==============================================================================
# BLOK 1: SİNFİN TƏYİNİ VƏ TUPLE (SABİT SİYAHI) SİNTAKSİSİ
# ==============================================================================
from datetime import datetime


class ConsoleInput:
    SUPPORTED_CURRENCIES: tuple[str, ...] = ("AZN", "USD", "EUR")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. `["AZN", "USD", "EUR"]` (list) vs `("AZN", "USD", "EUR")` (tuple) fərqi nədir?:
#    - Kvadrat mötərizə `[...]` dəyişdirilə bilən siyahıdır (`List<string>`):
#      içinə `.append()` ilə yeni element əlavə etmək olur.
#    - Dəyirmi mötərizə `(...)` isə `tuple`-dır (dəyişdirilə bilməyən / `ReadOnly` massiv):
#      yaradıldıqdan sonra nə element əlavə etmək, nə də silmək olur.
#    - `tuple[str, ...]` yazılışındakı `...` (üç nöqtə) "istənilən sayda `str`
#      elementi olan tuple" deməkdir (C#-dakı `readonly string[]`).
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: @STATICMETHOD (NİYƏ BURADA "SELF" YOXDUR?)
# ==============================================================================
    @staticmethod
    def get_positive_number(prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt))
                if value <= 0:
                    print("[Xəta] Məbləğ sıfırdan böyük olmalıdır! Yenidən cəhd edin.")
                    continue
                return value
            except ValueError:
                print("[Xəta] Zəhmət olmasa yalnız rəqəm daxil edin (məsələn: 25 və ya 14.50)!")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə bu metodda "self" YAZILMAYIB (`def get_positive_number(prompt: str)`)?:
#    - Çünki üzərinə `@staticmethod` qoyulub!
#    - Adi metodlar obyektə aid olduğu üçün 1-ci parametr kimi `self` (`this`) alır.
#    - C#-dakı `public static double GetPositiveNumber(string prompt)` metodunda necə ki
#      `this` yoxdur, Python-da da `@staticmethod` yazdıqda `self` yazılmır!
#    - Çağırılarkən də obyekt yaratmadan birbaşa sinif adı ilə çağırılır:
#      `ConsoleInput.get_positive_number("Məbləğ: ")`.
#
# 2. "value = float(input(prompt))":
#    - `input(prompt)` həm mesajı ekrana yazır (`Console.Write(prompt)`), həm də
#      istifadəçinin daxil etdiyi sətri oxuyub `str` kimi qaytarır (`Console.ReadLine()`).
#    - `float(...)` isə həmin mətni kəsr ədədə çevirir (`double.Parse(...)`).
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: @CLASSMETHOD VƏ "CLS" ("@STATICMETHOD"-DAN FƏRQİ NƏDİR?)
# ==============================================================================
    @classmethod
    def select_currency(cls) -> str:
        while True:
            choice = input("Valyutanı daxil edin (AZN / USD / EUR) [Susmaya görə AZN]: ").strip().upper()
            if choice == "":
                return "AZN"
            if choice in cls.SUPPORTED_CURRENCIES:
                return choice
            print(f"[Xəta] Yanlış valyuta! Yalnız bunlardan birini seçə bilərsiniz: {', '.join(cls.SUPPORTED_CURRENCIES)}")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "@staticmethod" ilə "@classmethod" arasındakı fərq nədir?:
#    - Hər ikisi C#-da `static` metod kimidir (obyekt yaratmadan `ConsoleInput.select_currency()`
#      kimi çağırılır).
#    - Fərq ondadır ki:
#      * `@staticmethod` sinfin içindəki heç bir başqa dəyişənə müraciət ETMİR (ona görə
#        mötərizədə nə `self`, nə də `cls` alır).
#      * `@classmethod` isə sinfin içindəki `SUPPORTED_CURRENCIES` sabitinə müraciət etmək
#        istəyir! Ona görə 1-ci parametr kimi sinfin özünü (`cls` = `ConsoleInput`) alır və
#        `cls.SUPPORTED_CURRENCIES` yazaraq həmin siyahını oxuyur.
#
# 2. "', '.join(cls.SUPPORTED_CURRENCIES)" necə işləyir?:
#    - C#-da `string.Join(", ", SupportedCurrencies)` yazırıq.
#    - Python-da isə birləşdirici simvol əvvəldə yazılır: `", ".join(siyahı)`.
#      Nəticədə `("AZN", "USD", "EUR")` siyahısını `"AZN, USD, EUR"` mətninə çevirir.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 4: TARİX YOXLANMASI VƏ "NONE" (NULL) QAYTARILMASI
# ==============================================================================
    @staticmethod
    def get_date() -> str | None:
        while True:
            date_input = input("Tarix (YYYY-MM-DD) [Boş buraxsanız bu gün seçiləcək]: ").strip()
            if date_input == "":
                return None
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                return date_input
            except ValueError:
                print("[Xəta] Yanlış tarix formatı! Nümunə: 2026-11-16 (İl-Ay-Gün).")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "-> str | None" və "return None":
#    - C#-dakı `public static string? GetDate()` və `return null;` qarşılığıdır.
#    - Python-da `null` əvəzinə `None` (böyük `N` hərfi ilə) yazılır.
#
# 2. "datetime.strptime(date_input, '%Y-%m-%d')":
#    - C#-dakı `DateTime.ParseExact(dateInput, "yyyy-MM-dd", ...)` metodudur.
#    - `%Y` -> 4 rəqəmli il (`yyyy`), `%m` -> 2 rəqəmli ay (`MM`), `%d` -> 2 rəqəmli gün (`dd`).
# ------------------------------------------------------------------------------
