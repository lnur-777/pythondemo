# -*- coding: utf-8 -*-
"""
Infrastructure Layer — Xarici REST API və Ehtiyat Valyuta Məzənnəsi Təminatçısı.
"""

# ==============================================================================
# BLOK 1: KİTABXANALARIN VƏ İNTERFEYSİN İMPORT EDİLMƏSİ
# ==============================================================================
import json
import urllib.error
import urllib.request
from interfaces.i_exchange_rate_provider import IExchangeRateProvider

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
# - `import json` vs `from interfaces... import IExchangeRateProvider`:
#   * Sadəcə `import json` yazdıqda kitabxananı bütöv gətiririk və içindəki
#     funksiyaları çağıranda `json.loads(...)` kimi nöqtə ilə yazırıq.
#   * `from ... import IExchangeRateProvider` yazdıqda isə həmin fayldan birbaşa
#     sinfin özünü gətiririk ki, aşağıda uzun-uzadı modul adı yazmayaq.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: İNTERFEYSDƏN MİRAS ALMA, SABİT LÜĞƏT VƏ KONSTRUKTOR
# ==============================================================================
class ApiExchangeRateProvider(IExchangeRateProvider):
    FALLBACK_RATES: dict[str, float] = {
        "AZN": 1.0,
        "USD": 1.70,
        "EUR": 1.85,
    }

    def __init__(self, api_url: str = "https://open.er-api.com/v6/latest/AZN") -> None:
        self.api_url = api_url

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "class ApiExchangeRateProvider(IExchangeRateProvider):":
#    - C#-dakı `public class ApiExchangeRateProvider : IExchangeRateProvider` sətridir.
#    - Python-da implement edilən interfeys mötərizə `(IExchangeRateProvider)` içində yazılır!
#
# 2. "FALLBACK_RATES: dict[str, float] = { ... }":
#    - Konstruktordan (`__init__`) kənarda, birbaşa `class` blokunun içində yazılan
#      dəyişən C#-dakı `static readonly` sahəyə bərabərdir (bütün obyektlər üçün ortaqdır).
#    - Böyük hərflərlə (`FALLBACK_RATES`) yazılması Python konvensiyasına görə onun
#      SABİT (Constant — dəyişdirilməməli) olduğunu bildirir.
#
# 3. "def __init__(self, api_url: str = 'https://...') -> None:":
#    - Konstruktordur. `api_url` parametrinə `=` ilə default dəyər verilib: əgər
#      `ApiExchangeRateProvider()` mötərizəsi boş çağırılarsa, həmin URL avtomatik götürülür.
#    - `self.api_url = api_url` sətri C#-dakı `this._apiUrl = apiUrl;` kimidir.
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: "WITH" (USING), "TRY / EXCEPT" VƏ "AND" SİNTAKSİSİ
# ==============================================================================
    def get_rates(self) -> dict[str, float]:
        print("\n[Sistem] Canlı valyuta məzənnələri yoxlanılır...")
        try:
            with urllib.request.urlopen(self.api_url, timeout=4) as response:
                raw_json = response.read().decode("utf-8")
                data = json.loads(raw_json)
                rates = data.get("rates", {})
                usd_rate = rates.get("USD")
                eur_rate = rates.get("EUR")

                if usd_rate and eur_rate:
                    live_rates = {
                        "AZN": 1.0,
                        "USD": round(1.0 / usd_rate, 4),
                        "EUR": round(1.0 / eur_rate, 4),
                    }
                    print(f"[Uğurlu] Canlı məzənnələr yükləndi: 1 USD = {live_rates['USD']} AZN | 1 EUR = {live_rates['EUR']} AZN")
                    return live_rates
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, Exception) as error:
            print(f"[Xəbərdarlıq] İnternet bağlantısı yoxdur və ya API əlçatmazdır ({error}).")
            print(f"[Sistem] Ehtiyat sabit məzənnələr istifadə olunur: 1 USD = {self.FALLBACK_RATES['USD']} AZN | 1 EUR = {self.FALLBACK_RATES['EUR']} AZN")

        return self.FALLBACK_RATES.copy()

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "with ... as response:" nədir?:
#    - C#-dakı `using (var response = ...)` ifadəsinin birbaşa qarşılığıdır!
#    - `with` blokunun içindəki (abzasla sağa çəkilmiş) sətirlər bitən kimi Python
#      şəbəkə bağlantısını avtomatik bağlayır (`response.Dispose()`).
#
# 2. "if usd_rate and eur_rate:":
#    - C#-da məntiqi "VƏ" operatoru `&&` kimi yazılır, Python-da isə sözlə `and` yazılır!
#    - Bu sətir yoxlayır ki, həm `usd_rate`, həm də `eur_rate` `None` (`null`) və ya `0` deyil.
#
# 3. "try:" və "except (...) as error:":
#    - C#-dakı `try { ... } catch (Exception error) { ... }` blokudur.
#    - Python-da `catch` əvəzinə `except` sözü işlənir, tutulan xəta dəyişəninin adı
#      isə `as error` kimi yazılır.
#    - Mötərizə içində bir neçə xəta tipini vergüllə yaza bilərik: bunlardan hər hansı
#      biri baş verərsə, həmin `except` bloku işə düşür.
#
# C#-DA NECƏ YAZILIR?:
# public Dictionary<string, double> GetRates()
# {
#     try
#     {
#         using var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(4) };
#         string rawJson = httpClient.GetStringAsync(_apiUrl).Result;
#         ...
#     }
#     catch (Exception error)
#     {
#         Console.WriteLine($"[Xəbərdarlıq] ({error.Message})");
#     }
#     return new Dictionary<string, double>(FallbackRates);
# }
# ------------------------------------------------------------------------------
