# -*- coding: utf-8 -*-
"""
Presentation Layer — Konsol İnterfeysi və Menyu İdarəedicisi (BudgetCliController).
"""

# ==============================================================================
# BLOK 1: KİTABXANALARIN İMPORTU, SİNFİN TƏYİNİ VƏ KONSTRUKTOR
# ==============================================================================
from datetime import datetime
from presentation.console_input import ConsoleInput
from services.budget_service import BudgetService


class BudgetCliController:
    def __init__(self, service: BudgetService) -> None:
        self._service = service

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. Niyə fiqurlu mötərizə "{ }" və nöqtəli-vergül ";" YOXDUR? Bəs metodun və ya
#    sinfin içi harada başlayıb harada bitir?:
#    - C#-da bloklar "{ }" ilə açılıb-bağlanır, sətirlər ";" ilə bitir.
#    - Python-da "{" əvəzinə sətrin sonunda qoşa nöqtə ":" qoyulur ("class BudgetCliController:",
#      "def __init__(...):").
#    - Blokun içi isə ABZASLA (Indentation — soldan 4 boşluq / 1 Tab) müəyyən edilir!
#    - "class BudgetCliController:" sətrindən sonra 4 boşluq içəridə yazılan bütün
#      "def ..." metodları bu sinfin İÇİNDƏ sayılır.
#    - "def __init__(...):" sətrindən sonra 8 boşluq (2 Tab) içəridə yazılan sətirlər
#      həmin metodun İÇİNDƏ sayılır. Növbəti sətir yenidən 4 boşluğa qayıdanda Python
#      başa düşür ki, əvvəlki metod BİTDİ (yəni C#-dakı bağlanan "}" işarəsi).
#    - Sətrin sonunda Enter (yeni sətir) avtomatik ";" rolunu oynayır.
#
# 2. Niyə "def" yazılır?:
#    - C#-da metod yazanda əvvəlcə qaytarılan tipi yazırıq ("public void RenderBalance()").
#    - Python-da isə bütün funksiya və metodlar məcburi olaraq "def" (define — təyin et)
#      açar sözü ilə başlayır.
#
# 3. Niyə konstruktorun adı sinfin adı deyil, "__init__" yazılır?:
#    - C#-da konstruktor sinfin öz adı ilə eyni olur ("public BudgetCliController(...)").
#    - Python-da konstruktorun adı HƏMİŞƏ "__init__" (initialize — ilkinləşdir) olur.
#    - Əvvəlində və sonunda iki alt xətt ("__") olan metodlara Python-da "dunder"
#      (double underscore) və ya "magic method" deyilir. Siz "BudgetCliController(service)"
#      yazanda Python arxa planda avtomatik bu "__init__" metodunu çağırır.
#
# 4. Niyə hər metodun birinci parametri "self" yazılır?:
#    - C#-da hər metodun içində gizli "this" açar sözü var ("this._service = service;").
#    - Python-da qayda belədir: "Gizli heç nə olmamalıdır". Ona görə C#-dakı "this"
#      obyektini Python-da hər metodun 1-ci parametri kimi açıq şəkildə "self" adı ilə
#      yazmaq MƏCBURİDİR ("def __init__(self, ...)", "def render_balance(self)").
#    - Amma metodu çağıranda "self" ötürülmür! Məsələn, "controller.render_balance()"
#      yazanda Python özü avtomatik "controller" obyektini "self"-in yerinə qoyur.
#
# 5. Niyə "_service" dəyişənini sinfin yuxarısında elan etmədik ("self._service = service")?:
#    - C#-da konstruktordan əvvəl sinfin içində "private readonly BudgetService _service;"
#      yazmalıyıq. Python-da isə "__init__" içində "self._service = service" yazdığımız
#      anda həmin obyektin içində "_service" adlı dəyişən (field) avtomatik yaranır!
#    - Python-da "public" / "private" açar sözləri yoxdur (hər şey default olaraq public-dir).
#      Dəyişənin əvvəlinə tək alt xətt ("_service") qoymaq C#-dakı "private" deməkdir
#      (digər proqramçılara və PyCharm-a "buna sinifdən kənarda toxunma" mesajı verir).
#
# 6. "service: BudgetService" və "-> None" nə deməkdir?:
#    - C#-da tip əvvəl, ad sonra gəlir: "BudgetService service".
#    - Python-da ad əvvəl, iki nöqtədən (:) sonra tip gəlir: "service: BudgetService".
#    - Metodun qaytardığı tip isə mötərizədən sonra "->" oxu ilə göstərilir: "-> None".
#      "None" burada C#-dakı "void" (heç nə qaytarmır) deməkdir.
#
# C#-DA NECƏ YAZILIR?:
# public class BudgetCliController
# {
#     private readonly BudgetService _service;
#
#     public BudgetCliController(BudgetService service)
#     {
#         this._service = service;
#     }
# }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 2: BALANS VƏ KATEQORİYA STATİSTİKASININ EKRANA ÇIXARILMASI
# ==============================================================================
    def render_balance(self) -> None:
        summary = self._service.get_balance_summary()
        print("\n" + "=" * 45)
        print("           CARİ MALİYYƏ BALANSI")
        print("=" * 45)
        print(f"Ümumi Gəlir : {summary.total_income:.2f} AZN")
        print(f"Ümumi Xərc  : {summary.total_expense:.2f} AZN")
        print("-" * 45)
        print(f"Xalis Balans: {summary.net_balance:.2f} AZN")
        print(f"Status      : {summary.status_message}")
        print("=" * 45)

    def render_category_statistics(self) -> None:
        stats, total_expense = self._service.get_category_statistics()
        print("\n" + "=" * 50)
        print("       KATEQORİYALAR ÜZRƏ XƏRC STATİSTİKASI")
        print("=" * 50)

        if total_expense == 0:
            print("Hələ heç bir xərc qeydə alınmayıb.")
            print("=" * 50)
            return

        for category, amount, percentage in stats:
            bar = "#" * int(percentage // 5)
            print(f"{category:<15} | {amount:>8.2f} AZN | {percentage:>5.1f}% | {bar}")

        print("-" * 50)
        print(f"CƏMİ XƏRC       | {total_expense:>8.2f} AZN | 100.0%")
        print("=" * 50)

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "def render_balance(self) -> None:":
#    - C#-dakı "public void RenderBalance()" metodudur. Kənardan parametr almır, amma
#      sinfin öz daxili "self._service" dəyişəninə çata bilmək üçün mötərizədə "self" yazılır.
#
# 2. "stats, total_expense = self._service.get_category_statistics()":
#    - Tuple Unpacking (C#-da Tuple Deconstruction: "var (stats, totalExpense) = ...").
#      Metod iki dəyər qaytarır və biz onları vergüllə birbaşa iki ayrı dəyişənə mənimsədirik.
#
# 3. "if total_expense == 0:":
#    - C#-dan fərqli olaraq Python-da "if" şərtini mötərizə "( )" içinə almaq məcburi DEYİL!
#    - Şərtin sonunda ":" qoyulur və "if"-in içindəki 3 sətir 4 boşluq sağa sürüşdürülür.
#      "return"-dən sonrakı "for" sətri yenidən sola qayıtdığı üçün Python bilir ki,
#      "if" bloku artıq bitib!
#
# 4. "for category, amount, percentage in stats:":
#    - C#-dakı "foreach (var (category, amount, percentage) in stats)" dövrüdür.
#    - Python-da klassik "for (int i=0; i<n; i++)" yoxdur; bütün "for" dövrləri
#      C#-dakı "foreach" kimi işləyir ("for dəyişən in siyahı:").
#
# 5. '"=" * 45' və "percentage // 5":
#    - Python-da string-i ədədə vurmaq ("=" * 45) həmin simvolu 45 dəfə təkrarlayır.
#    - Python-da tək "/" bölmə həmişə kəsr ədəd verir (məs: 10 / 2 = 5.0).
#      C#-dakı tam bölməni (kəsr hissəni atmağı) etmək üçün qoşa "//" yazılır ("percentage // 5").
#
# 6. 'f"... {category:<15} | {amount:>8.2f} ..."':
#    - dırnaqdan əvvəlki "f" hərfi C#-dakı "$" işarəsidir ($"...").
#    - "{category:<15}" -> C#-da "{category,-15}" (15 simvol yer ayır, sola düzləndir).
#    - "{amount:>8.2f}" -> C#-da "{amount,8:F2}" (8 simvol yer ayır, sağa düzləndir,
#      vergüldən sonra 2 rəqəm göstər).
#
# C#-DA NECƏ YAZILIR?:
# public void RenderCategoryStatistics()
# {
#     var (stats, totalExpense) = _service.GetCategoryStatistics();
#     if (totalExpense == 0)
#     {
#         Console.WriteLine("Hələ heç bir xərc qeydə alınmayıb.");
#         return;
#     }
#     foreach (var (category, amount, percentage) in stats)
#     {
#         string bar = new string('#', (int)(percentage / 5));
#         Console.WriteLine($"{category,-15} | {amount,8:F2} AZN | {percentage,5:F1}% | {bar}");
#     }
# }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 3: AYLIQ HESABAT VƏ BÜTÜN ƏMƏLİYYATLAR TARİXÇƏSİ
# ==============================================================================
    def render_monthly_report(self, year_month: str) -> None:
        report = self._service.get_monthly_report(year_month)
        print("\n" + "=" * 55)
        print(f"             AYLIQ HESABAT ({year_month})")
        print("=" * 55)

        if not report.transactions:
            print(f"'{year_month}' tarixi üçün heç bir əməliyyat tapılmadı.")
            print("=" * 55)
            return

        print(f"Əməliyyat sayı : {len(report.transactions)}")
        print(f"Aylıq Gəlir    : {report.monthly_income:.2f} AZN")
        print(f"Aylıq Xərc     : {report.monthly_expense:.2f} AZN")
        print(f"Aylıq Qalıq    : {(report.monthly_income - report.monthly_expense):.2f} AZN")

        if report.largest_expense:
            le = report.largest_expense
            print(f"Ən böyük xərc  : {le.amount_azn:.2f} AZN ({le.category} - {le.description})")

        print("-" * 55)
        print("Tarix      | Növ   | Kateqoriya   | Məbləğ (AZN) | Açıqlama")
        print("-" * 55)
        for tx in report.transactions:
            sign = "+" if tx.transaction_type == "gelir" else "-"
            print(f"{tx.date} | {tx.transaction_type.upper():<5} | {tx.category:<12} | {sign}{tx.amount_azn:>10.2f} | {tx.description}")
        print("=" * 55)

    def render_all_transactions(self) -> None:
        print("\n" + "=" * 65)
        print("                    BÜTÜN ƏMƏLİYYATLAR TARİXÇƏSİ")
        print("=" * 65)
        if not self._service.transactions:
            print("Bazaya hələ heç bir əməliyyat daxil edilməyib.")
            print("=" * 65)
            return

        for index, tx in enumerate(self._service.transactions, start=1):
            sign = "+" if tx.transaction_type == "gelir" else "-"
            original = f"({tx.amount} {tx.currency})" if tx.currency != "AZN" else ""
            print(f"{index:>2}. [{tx.date}] {tx.transaction_type.upper():<5} | {tx.category:<12} | {sign}{tx.amount_azn:.2f} AZN {original} | {tx.description}")
        print("=" * 65)

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "if not report.transactions:" və "if report.largest_expense:":
#    - C#-da məntiqi inkar "!" işarəsidir, Python-da isə sözlə "not" yazılır.
#    - Python-da boş siyahı ("[]"), boş sətir ("") və "None" ("null") avtomatik
#      "False" sayılır ("Truthy / Falsy" qaydası).
#    - Ona görə "if report.transactions.Count == 0" əvəzinə "if not report.transactions:"
#      yazırıq; "if report.largest_expense != null" əvəzinə isə sadəcə
#      "if report.largest_expense:" yazırıq!
#
# 2. "len(report.transactions)":
#    - C#-da siyahının uzunluğu üçün ".Count" və ya ".Length" yazılır.
#    - Python-da isə bütün siyahıların və mətnlərin uzunluğu qlobal "len(...)"
#      funksiyası ilə tapılır.
#
# 3. "sign = '+' if tx.transaction_type == 'gelir' else '-'":
#    - Ternary operator: C#-da şərt birinci gəlir (`şərt ? dəyər1 : dəyər2`).
#    - Python-da isə oxunaqlı ingilis cümləsi kimi yazılır:
#      `dəyər1 if şərt else dəyər2` ("əgər şərt doğrudursa '+', əks halda '-'").
#
# 4. "for index, tx in enumerate(self._service.transactions, start=1):":
#    - "enumerate" siyahıdakı hər elementi nömrələyir: 1-ci dəyişənə ("index") sıra
#      nömrəsini (1, 2, 3...), 2-ci dəyişənə ("tx") isə obyektin özünü verir.
#
# C#-DA NECƏ YAZILIR?:
# if (!report.Transactions.Any()) return;
# Console.WriteLine($"Əməliyyat sayı : {report.Transactions.Count}");
# if (report.LargestExpense != null) { ... }
# foreach (var tx in report.Transactions)
# {
#     string sign = tx.TransactionType == "gelir" ? "+" : "-";
#     ...
# }
# ------------------------------------------------------------------------------


# ==============================================================================
# BLOK 4: ƏMƏLİYYAT ƏLAVƏ ETMƏ, KALKULYATOR VƏ ƏSAS MENYU DÖVRÜ (RUN)
# ==============================================================================
    def handle_add_transaction(self, choice: str) -> None:
        transaction_type = "gelir" if choice == "1" else "xerc"
        header = "GƏLİR" if transaction_type == "gelir" else "XƏRC"
        print(f"\n--- YENİ {header} ƏLAVƏ EDİLİR ---")

        amount = ConsoleInput.get_positive_number("Məbləği daxil edin: ")
        currency = ConsoleInput.select_currency()

        if transaction_type == "gelir":
            category = input("Kateqoriya (məs: Maaş, Bonus, Freelance): ").strip() or "Digər Gəlir"
        else:
            category = input("Kateqoriya (məs: Qida, Nəqliyyat, Kommunal, Əyləncə): ").strip() or "Digər Xərc"

        description = input("Qısa açıqlama (istəyə bağlı): ").strip()
        date = ConsoleInput.get_date()

        tx = self._service.add_transaction(transaction_type, amount, currency, category, description, date)
        print(f"\n[OK] Əməliyyat əlavə edildi: {amount} {tx.currency} ({tx.amount_azn} AZN) - {category}")

    def handle_currency_converter(self) -> None:
        print("\n--- VALYUTA KALKULYATORU ---")
        amount = ConsoleInput.get_positive_number("Çevirmək istədiyiniz məbləğ: ")
        currency = ConsoleInput.select_currency()
        result_azn = self._service.convert_to_azn(amount, currency)
        print(f"Nəticə: {amount} {currency} = {result_azn:.2f} AZN")

    def run(self) -> None:
        while True:
            print("\n" + "*" * 45)
            print("  AĞILLI ŞƏXSİ BÜDCƏ VƏ VALYUTA İZLƏYİCİSİ")
            print("*" * 45)
            print("1. Gəlir əlavə et")
            print("2. Xərc əlavə et")
            print("3. Cari balansı göstər")
            print("4. Kateqoriyalar üzrə xərc statistikası")
            print("5. Aylıq hesabat")
            print("6. Bütün əməliyyatların tarixçəsi")
            print("7. Valyuta çevirici (Kalkulyator)")
            print("0. Çıxış")
            print("*" * 45)

            choice = input("Seçiminizi daxil edin (0-7): ").strip()

            if choice in ("1", "2"):
                self.handle_add_transaction(choice)
            elif choice == "3":
                self.render_balance()
            elif choice == "4":
                self.render_category_statistics()
            elif choice == "5":
                current_month = datetime.now().strftime("%Y-%m")
                year_month = input(f"Hesabat ayını daxil edin (YYYY-MM) [Cari ay üçün Enter basın: {current_month}]: ").strip() or current_month
                self.render_monthly_report(year_month)
            elif choice == "6":
                self.render_all_transactions()
            elif choice == "7":
                self.handle_currency_converter()
            elif choice == "0":
                print("\nMəlumatlarınız yadda saxlanıldı. Proqramdan çıxılır. Uğurlar!")
                break
            else:
                print("\n[Xəta] Yanlış seçim! Zəhmət olmasa 0 ilə 7 arasında bir rəqəm daxil edin.")

# ------------------------------------------------------------------------------
# SİNTAKSİS İZAHI (.NET / C# ilə fərqlər):
#
# 1. "while True:":
#    - C#-da boolean dəyərlər kiçik hərflə ("true", "false") yazılır.
#    - Python-da isə böyük baş hərflə ("True", "False") yazılması MƏCBURİDİR!
#
# 2. "if ... elif ... else:":
#    - C#-dakı "else if" Python-da qısaldılaraq "elif" kimi yazılır.
#    - Diqqət edin: həm "if", həm "elif", həm də "else" sətirlərinin sonunda ":" var
#      və hər birinin gövdəsi 4 boşluq sağa çəkilib.
#
# 3. "if choice in ('1', '2'):":
#    - C#-da "if (choice == "1" || choice == "2")" yazırıq.
#    - Python-da "in" operatoru ilə dəyərin verilmiş siyahıda olub-olmadığını
#      yoxlamaq çox rahatdır: "choice dəyəri ('1', '2') içindədirmi?".
#
# 4. "input('...').strip() or 'Digər Gəlir'":
#    - Python-da məntiqi VƏ YA operatoru "||" deyil, sözlə "or" yazılır.
#    - Əgər istifadəçi heç nə yazmayıb Enter basarsa, sol tərəf boş sətir ("") olur,
#      "or" operatoru isə dərhal sağ tərəfdəki default mətni ("Digər Gəlir") qaytarır.
#
# 5. "self.render_balance()":
#    - C#-da eyni sinfin içindəki başqa metodu çağıranda sadəcə "RenderBalance();"
#      yaza bilirik ("this." yazmaq məcburi deyil).
#    - Python-da isə eyni sinfin başqa metodunu və ya dəyişənini çağıranda qarşısında
#      "self." yazmaq MƏCBURİDİR ("self.render_balance()"). Əks halda Python onu
#      sinifdən kənar qlobal funksiya kimi axtaracaq!
# ------------------------------------------------------------------------------
