# -*- coding: utf-8 -*-
"""
Ağıllı Şəxsi Büdcə və Valyuta İzləyicisi — Giriş Nöqtəsi (C#-dakı Program.cs qarşılığı)
"""

# ==============================================================================
# BLOK 1: MODULLARIN VƏ SİNİFLƏRİN İMPORT EDİLMƏSİ
# ==============================================================================
from infrastructure.api_exchange_rate_provider import ApiExchangeRateProvider
from infrastructure.json_transaction_repository import JsonTransactionRepository
from interfaces.i_exchange_rate_provider import IExchangeRateProvider
from interfaces.i_transaction_repository import ITransactionRepository
from presentation.budget_cli_controller import BudgetCliController
from services.budget_service import BudgetService

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "from qovluq.fayl_adi import SinifAdi" nə deməkdir?:
#    - C#-da faylın adı önəmli deyil, biz sadəcə "using AgilliBudce.Services;"
#      (namespace adını) yazırıq.
#    - Python-da isə "namespace" anlayışını QOVLUQLAR və FAYLLAR əvəz edir!
#    - Məsələn, "from services.budget_service import BudgetService" sətirində:
#      * "services"      -> qovluğun adıdır
#      * "budget_service"-> həmin qovluqdakı "budget_service.py" faylının adıdır
#      * "BudgetService" -> həmin faylın içindəki "class BudgetService" sinfidir.
#
# 2. Niyə sətrin sonunda ";" yoxdur?:
#    - Python-da əmrin bitdiyini ";" deyil, yeni sətrə keçmək (Enter) bildirir.
#
# C#-DA NECƏ YAZILIR?:
# using AgilliBudce.Infrastructure;
# using AgilliBudce.Interfaces;
# using AgilliBudce.Presentation;
# using AgilliBudce.Services;
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: MAIN FUNKSİYASI VƏ OBYEKTLƏRİN YARADILMASI
# ==============================================================================
def main() -> None:
    rate_provider: IExchangeRateProvider = ApiExchangeRateProvider()
    repository: ITransactionRepository = JsonTransactionRepository()
    service = BudgetService(repository=repository, rate_provider=rate_provider)
    controller = BudgetCliController(service=service)
    controller.run()

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə "def main() -> None:" yazılır və "{ }" mötərizələri haradadır?:
#    - "def": Python-da istənilən funksiya və ya metod "def" (define) sözü ilə başlayır.
#    - "-> None": Funksiyanın geri qaytardığı tip mötərizədən sonra "->" oxu ilə
#      yazılır. "None" burada C#-dakı "void" deməkdir (funksiya heç nə qaytarmır).
#    - ":" (Qoşa nöqtə): C#-da funksiyanın gövdəsini açan "{" mötərizəsinin əvəzidir!
#    - Abzas (Indentation): ":" işarəsindən sonra gələn və soldan 4 boşluq (1 Tab)
#      içəridə yazılan 5 sətir "main()" funksiyasının İÇİNDƏ sayılır. Soldan boşluq
#      bitən kimi (növbəti blokda) funksiya da bitmiş sayılır (C#-dakı "}" əvəzi).
#
# 2. Niyə "rate_provider: IExchangeRateProvider = ApiExchangeRateProvider()" sətrində
#    "new" açar sözü YOXDUR və tip sağda yazılıb?:
#    - C#-da əvvəl tipi, sonra dəyişən adını yazırıq:
#      "IExchangeRateProvider rateProvider"
#    - Python-da isə əvvəl dəyişən adı, sonra ":" qoyulub tipi yazılır:
#      "rate_provider: IExchangeRateProvider"
#    - Obyekt yaradarkən Python-da "new" sözü mövcud deyil! Sadəcə sinfin adını
#      yazıb mötərizə açmaq ("ApiExchangeRateProvider()") C#-dakı "new ApiExchangeRateProvider()"
#      ilə eyni işi görür.
#
# 3. "BudgetService(repository=repository, rate_provider=rate_provider)" nədir?:
#    - Python-da arqumentləri ötürərkən parametr adını açıq yaza bilərik
#      (C#-dakı Named Arguments: "new BudgetService(repository: repository, ...)").
#    - İstəsəniz qısaca "BudgetService(repository, rate_provider)" də yaza bilərsiniz.
#
# C#-DA NECƏ YAZILIR?:
# static void Main(string[] args)
# {
#     IExchangeRateProvider rateProvider = new ApiExchangeRateProvider();
#     ITransactionRepository repository = new JsonTransactionRepository();
#     var service = new BudgetService(repository, rateProvider);
#     var controller = new BudgetCliController(service);
#     controller.Run();
# }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: PROQRAMIN BAŞLANĞIC NÖQTƏSİ (IF __NAME__ == "__MAIN__")
# ==============================================================================
if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. C#-da kompilator "static void Main()" adlı metodu görən kimi proqramı avtomatik
#    oradan başladır. Bəs Python-da niyə bu "if" sətrini yazmalıyıq?:
#    - Python-da "main()" xüsusi açar söz deyil, adi bir funksiyadır. Əgər onu
#      aşağıda çağırmasaq, proqram heç nə etmədən dayanacaq!
#    - "__name__" Python-un öz daxili (built-in) dəyişənidir.
#    - Siz birbaşa bu faylı "Run" etdikdə Python avtomatik olaraq `__name__` dəyişəninə
#      `"__main__"` mətnini mənimsədir və şərt doğru olduğu üçün `main()` çağırılır.
#    - Bəs niyə birbaşa `main()` yazmayıb `if __name__ == "__main__":` içində yazırıq?
#      Çünki başqa bir fayl bu faylı `import` etsə, `main()` özbaşına işə düşməsin,
#      yalnız bu fayl birbaşa Run ediləndə işləsin.
# ------------------------------------------------------------------------------
