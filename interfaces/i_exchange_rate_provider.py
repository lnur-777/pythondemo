# -*- coding: utf-8 -*-
"""
Interfaces Layer — Valyuta Məzənnəsi Təminatçısı İnterfeysi (IExchangeRateProvider).
"""

# ==============================================================================
# BLOK 1: PYTHON-DA INTERFACE YARATMA SİNTAKSİSİ (ABC VƏ @ABSTRACTMETHOD)
# ==============================================================================
from abc import ABC, abstractmethod


class IExchangeRateProvider(ABC):
    @abstractmethod
    def get_rates(self) -> dict[str, float]:
        pass

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə "interface IExchangeRateProvider" yazmadıq, "class ...(ABC):" yazdıq?:
#    - Python dilində `interface` adlı açar söz YOXDUR!
#    - Python-da interfeys (və ya abstract class) yaratmaq üçün standart `abc`
#      (Abstract Base Classes) kitabxanasındakı `ABC` sinfindən miras alınır.
#
# 2. Miras almaq (Inheritance) niyə `:` ilə yox, mötərizə `(ABC)` ilə yazılır?:
#    - C#-da miras və interfeys implementasiyası `:` ilə yazılır:
#      `public class MyClass : BaseClass`
#    - Python-da `:` işarəsi artıq blok açmaq (`{` əvəzi) üçün məşğuldur!
#    - Ona görə Python-da miras alınan sinif və ya interfeys mötərizə içində yazılır:
#      `class IExchangeRateProvider(ABC):`
#
# 3. "@abstractmethod" və "pass" nə üçündür?:
#    - `@abstractmethod` bu metodun gövdəsiz (abstrakt) olduğunu bildirir: bu sinifdən
#      miras alan hər bir sinif `get_rates` metodunu MƏCBURİ yazmalıdır (override etməlidir).
#    - Bəs niyə aşağıda `pass` yazılıb?
#      C#-da interfeys metodunun sonunda sadəcə `;` qoyub bitiririk (`Dictionary<string, double> GetRates();`).
#      Python-da isə `:` işarəsindən sonra mütləq abzasla (8 boşluq içəridə) ən azı 1 sətir
#      kod yazılmalıdır — boş saxlamaq sintaksis xətasıdır!
#      Ona görə Python-da "burada heç bir əməliyyat yoxdur, boş gövdədir" demək üçün
#      xüsusi `pass` açar sözü yazılıb.
#
# C#-DA NECƏ YAZILIR?:
# public interface IExchangeRateProvider
# {
#     Dictionary<string, double> GetRates();
# }
# ------------------------------------------------------------------------------
