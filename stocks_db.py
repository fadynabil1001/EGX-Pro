"""
قاعدة بيانات الأسهم المصرية - EGX Stocks Database
يحتوي على قائمة شاملة بأسهم البورصة المصرية مع الأسماء العربية والإنجليزية
ورموز TradingView و Investing.com و Yahoo Finance
"""

# ====================================================================
# قائمة الأسهم المصرية الرئيسية
# Symbol structure:
#   - ticker: EGX ticker symbol (used by EGX, Mubasher)
#   - yahoo: Yahoo Finance suffix (.CA for Cairo)
#   - tv: TradingView symbol (EGX:TICKER)
#   - name_ar: Arabic name
#   - name_en: English name
#   - sector: Industry sector
#   - investing_slug: Investing.com URL slug for fetching
# ====================================================================

EGX_STOCKS = [
    # ============== EGX 30 Constituents ==============
    {
        "ticker": "COMI", "yahoo": "COMI.CA", "tv": "EGX:COMI",
        "name_ar": "البنك التجاري الدولي - مصر", "name_en": "Commercial International Bank",
        "sector": "Banks", "investing_slug": "com-intl-bk"
    },
    {
        "ticker": "EFIH", "yahoo": "EFIH.CA", "tv": "EGX:EFIH",
        "name_ar": "إي فاينانس للاستثمارات المالية والرقمية", "name_en": "E-Finance",
        "sector": "Technology", "investing_slug": "e-finance-digital-financial-invest"
    },
    {
        "ticker": "HRHO", "yahoo": "HRHO.CA", "tv": "EGX:HRHO",
        "name_ar": "المجموعة المالية هيرميس القابضة", "name_en": "EFG Hermes Holdings",
        "sector": "Financial Services", "investing_slug": "efg-hermes-hol"
    },
    {
        "ticker": "TMGH", "yahoo": "TMGH.CA", "tv": "EGX:TMGH",
        "name_ar": "مجموعة طلعت مصطفى القابضة", "name_en": "Talaat Moustafa Group",
        "sector": "Real Estate", "investing_slug": "t-m-g-holding"
    },
    {
        "ticker": "ETEL", "yahoo": "ETEL.CA", "tv": "EGX:ETEL",
        "name_ar": "المصرية للاتصالات", "name_en": "Telecom Egypt",
        "sector": "Telecommunications", "investing_slug": "telecom-egypt"
    },
    {
        "ticker": "EAST", "yahoo": "EAST.CA", "tv": "EGX:EAST",
        "name_ar": "الشرقية - ايسترن كومباني", "name_en": "Eastern Tobacco",
        "sector": "Tobacco", "investing_slug": "eastern-co"
    },
    {
        "ticker": "FWRY", "yahoo": "FWRY.CA", "tv": "EGX:FWRY",
        "name_ar": "فوري لتكنولوجيا البنوك والمدفوعات الإلكترونية", "name_en": "Fawry",
        "sector": "Technology", "investing_slug": "fawry-banking-and-payment"
    },
    {
        "ticker": "ABUK", "yahoo": "ABUK.CA", "tv": "EGX:ABUK",
        "name_ar": "أبوقير للأسمدة والصناعات الكيماوية", "name_en": "Abu Qir Fertilizers",
        "sector": "Chemicals", "investing_slug": "abou-kir-fertilizers"
    },
    {
        "ticker": "ORAS", "yahoo": "ORAS.CA", "tv": "EGX:ORAS",
        "name_ar": "أوراسكوم كونستراكشون بي إل سي", "name_en": "Orascom Construction",
        "sector": "Construction", "investing_slug": "orascom-construction-ltd"
    },
    {
        "ticker": "PHDC", "yahoo": "PHDC.CA", "tv": "EGX:PHDC",
        "name_ar": "بالم هيلز للتعمير", "name_en": "Palm Hills Development",
        "sector": "Real Estate", "investing_slug": "palm-hill-dev"
    },
    {
        "ticker": "EMFD", "yahoo": "EMFD.CA", "tv": "EGX:EMFD",
        "name_ar": "إعمار مصر للتنمية", "name_en": "Emaar Misr",
        "sector": "Real Estate", "investing_slug": "emaar-misr-for-development-sae"
    },
    {
        "ticker": "JUFO", "yahoo": "JUFO.CA", "tv": "EGX:JUFO",
        "name_ar": "جهينة للصناعات الغذائية", "name_en": "Juhayna Food Industries",
        "sector": "Food & Beverages", "investing_slug": "juhayna-food-industries"
    },
    {
        "ticker": "EKHO", "yahoo": "EKHO.CA", "tv": "EGX:EKHO",
        "name_ar": "القابضة المصرية الكويتية", "name_en": "Egypt Kuwait Holding",
        "sector": "Investments", "investing_slug": "egypt-kuwait-holding"
    },
    {
        "ticker": "EKHOA", "yahoo": "EKHOA.CA", "tv": "EGX:EKHOA",
        "name_ar": "القابضة المصرية الكويتية - دولار", "name_en": "EKH-USD",
        "sector": "Investments", "investing_slug": "egypt-kuwait-h"
    },
    {
        "ticker": "EFID", "yahoo": "EFID.CA", "tv": "EGX:EFID",
        "name_ar": "إديتا للصناعات الغذائية", "name_en": "Edita Food Industries",
        "sector": "Food & Beverages", "investing_slug": "edita-food-industries"
    },
    {
        "ticker": "ESRS", "yahoo": "ESRS.CA", "tv": "EGX:ESRS",
        "name_ar": "حديد عز", "name_en": "Ezz Steel",
        "sector": "Steel & Iron", "investing_slug": "al-ezz-steel-rebars"
    },
    {
        "ticker": "SWDY", "yahoo": "SWDY.CA", "tv": "EGX:SWDY",
        "name_ar": "السويدي إليكتريك", "name_en": "Elsewedy Electric",
        "sector": "Electrical Equipment", "investing_slug": "el-swedy-cables"
    },
    {
        "ticker": "AMOC", "yahoo": "AMOC.CA", "tv": "EGX:AMOC",
        "name_ar": "الإسكندرية للزيوت المعدنية", "name_en": "Alexandria Mineral Oils",
        "sector": "Oil & Gas", "investing_slug": "alx-mineral-oi"
    },
    {
        "ticker": "ADIB", "yahoo": "ADIB.CA", "tv": "EGX:ADIB",
        "name_ar": "مصرف أبوظبي الإسلامي - مصر", "name_en": "Abu Dhabi Islamic Bank Egypt",
        "sector": "Banks", "investing_slug": "abu-dhabi-islamic-bank-egypt"
    },
    {
        "ticker": "EGAL", "yahoo": "EGAL.CA", "tv": "EGX:EGAL",
        "name_ar": "مصر للألمونيوم", "name_en": "Egypt Aluminum",
        "sector": "Metals", "investing_slug": "egypt-aluminum"
    },
    {
        "ticker": "ORHD", "yahoo": "ORHD.CA", "tv": "EGX:ORHD",
        "name_ar": "أوراسكوم للتنمية مصر", "name_en": "Orascom Development Egypt",
        "sector": "Hotels & Tourism", "investing_slug": "orascom-hotels-and-development"
    },
    {
        "ticker": "OIH", "yahoo": "OIH.CA", "tv": "EGX:OIH",
        "name_ar": "أوراسكوم للاستثمار القابضة", "name_en": "Orascom Investment Holding",
        "sector": "Investments", "investing_slug": "orascom-telecom-media---technology"
    },
    {
        "ticker": "ORWE", "yahoo": "ORWE.CA", "tv": "EGX:ORWE",
        "name_ar": "النساجون الشرقيون للسجاد", "name_en": "Oriental Weavers",
        "sector": "Textiles", "investing_slug": "oriental-weave"
    },
    {
        "ticker": "MCQE", "yahoo": "MCQE.CA", "tv": "EGX:MCQE",
        "name_ar": "مصر بني سويف للأسمنت", "name_en": "Misr Cement",
        "sector": "Cement", "investing_slug": "misr-cement-qe"
    },
    {
        "ticker": "CCAP", "yahoo": "CCAP.CA", "tv": "EGX:CCAP",
        "name_ar": "القلعة القابضة للاستثمارات المالية", "name_en": "Qalaa Holdings",
        "sector": "Investments", "investing_slug": "citadel-capita"
    },
    {
        "ticker": "AUTO", "yahoo": "AUTO.CA", "tv": "EGX:AUTO",
        "name_ar": "جي بي أوتو", "name_en": "GB Auto",
        "sector": "Automotive", "investing_slug": "gb-auto-s.a.e"
    },
    {
        "ticker": "ISPH", "yahoo": "ISPH.CA", "tv": "EGX:ISPH",
        "name_ar": "ابن سينا فارما", "name_en": "Ibnsina Pharma",
        "sector": "Healthcare", "investing_slug": "ibnsina-pharma"
    },
    {
        "ticker": "RAYA", "yahoo": "RAYA.CA", "tv": "EGX:RAYA",
        "name_ar": "راية القابضة للاستثمارات المالية", "name_en": "Raya Holding",
        "sector": "Technology", "investing_slug": "raya-tech---co"
    },
    {
        "ticker": "BTFH", "yahoo": "BTFH.CA", "tv": "EGX:BTFH",
        "name_ar": "بلتون المالية القابضة", "name_en": "Beltone Financial Holding",
        "sector": "Financial Services", "investing_slug": "beltone-financial-holding"
    },
    {
        "ticker": "HELI", "yahoo": "HELI.CA", "tv": "EGX:HELI",
        "name_ar": "مصر الجديدة للإسكان والتعمير", "name_en": "Heliopolis Housing",
        "sector": "Real Estate", "investing_slug": "heliopolis-housing"
    },
    {
        "ticker": "KIMA", "yahoo": "KIMA.CA", "tv": "EGX:KIMA",
        "name_ar": "الصناعات الكيماوية المصرية كيما", "name_en": "Egypt Chemical Industries (Kima)",
        "sector": "Chemicals", "investing_slug": "egypt-chem-ind"
    },
    {
        "ticker": "ACGC", "yahoo": "ACGC.CA", "tv": "EGX:ACGC",
        "name_ar": "الأسمنت العربية", "name_en": "Arabian Cement",
        "sector": "Cement", "investing_slug": "arabian-cement-co-sae"
    },
    {
        "ticker": "ARCC", "yahoo": "ARCC.CA", "tv": "EGX:ARCC",
        "name_ar": "العاشر من رمضان للصناعات الدوائية", "name_en": "Tenth of Ramadan Pharma",
        "sector": "Healthcare", "investing_slug": "tenth-of-ramadan-for-pharmaceutical"
    },

    # ============== EGX 70 - Additional Constituents ==============
    {
        "ticker": "OFH", "yahoo": "OFH.CA", "tv": "EGX:OFH",
        "name_ar": "المالية والصناعية المصرية", "name_en": "Egyptian Financial Industrial",
        "sector": "Industrial", "investing_slug": "egyptian-financial-and-industrial"
    },
    {
        "ticker": "CIEB", "yahoo": "CIEB.CA", "tv": "EGX:CIEB",
        "name_ar": "البنك المصري لتنمية الصادرات", "name_en": "Export Development Bank",
        "sector": "Banks", "investing_slug": "egyptian-export-bank"
    },
    {
        "ticker": "HRHOA", "yahoo": "HRHOA.CA", "tv": "EGX:HRHOA",
        "name_ar": "هيرميس - دولار", "name_en": "EFG Hermes USD",
        "sector": "Financial Services", "investing_slug": "efg-hermes"
    },
    {
        "ticker": "CIRA", "yahoo": "CIRA.CA", "tv": "EGX:CIRA",
        "name_ar": "كايرو للاستثمار والتنمية العقارية", "name_en": "CIRA Education",
        "sector": "Education", "investing_slug": "cairo-investment-and-real-estate-development-co"
    },
    {
        "ticker": "OCDI", "yahoo": "OCDI.CA", "tv": "EGX:OCDI",
        "name_ar": "السادس من اكتوبر للتنمية والاستثمار", "name_en": "Six of October Dev. (SODIC)",
        "sector": "Real Estate", "investing_slug": "six-of-october-dev"
    },
    {
        "ticker": "MNHD", "yahoo": "MNHD.CA", "tv": "EGX:MNHD",
        "name_ar": "مدينة نصر للإسكان والتعمير", "name_en": "Madinet Nasr Housing",
        "sector": "Real Estate", "investing_slug": "medinet-nasr-housing-and-development"
    },
    {
        "ticker": "MFPC", "yahoo": "MFPC.CA", "tv": "EGX:MFPC",
        "name_ar": "مصر للأسمدة - موبكو", "name_en": "Misr Fertilizers (MOPCO)",
        "sector": "Chemicals", "investing_slug": "misr-fertilizers-production-co"
    },
    {
        "ticker": "SKPC", "yahoo": "SKPC.CA", "tv": "EGX:SKPC",
        "name_ar": "سيدي كرير للبتروكيماويات", "name_en": "Sidi Kerir Petrochemicals (Sidpec)",
        "sector": "Petrochemicals", "investing_slug": "sidi-kerir-petrochemicals"
    },
    {
        "ticker": "MTIE", "yahoo": "MTIE.CA", "tv": "EGX:MTIE",
        "name_ar": "إم إم جروب للصناعة والتجارة العالمية", "name_en": "MM Group",
        "sector": "Industrial", "investing_slug": "mtie-corp"
    },
    {
        "ticker": "DSCW", "yahoo": "DSCW.CA", "tv": "EGX:DSCW",
        "name_ar": "دايس للملابس الجاهزة", "name_en": "Dice Sports & Casual Wear",
        "sector": "Textiles", "investing_slug": "dice-sport---casual-wear"
    },
    {
        "ticker": "EGCH", "yahoo": "EGCH.CA", "tv": "EGX:EGCH",
        "name_ar": "الكابلات الكهربائية المصرية", "name_en": "Egyptian Electric Cables",
        "sector": "Electrical Equipment", "investing_slug": "el-sewedy-electrometer"
    },
    {
        "ticker": "AIH", "yahoo": "AIH.CA", "tv": "EGX:AIH",
        "name_ar": "الإسكندرية للاستثمار العقاري", "name_en": "Alex. Investment",
        "sector": "Real Estate", "investing_slug": "alexandria-investment-real-estate"
    },
    {
        "ticker": "MASR", "yahoo": "MASR.CA", "tv": "EGX:MASR",
        "name_ar": "مدينة مصر للإسكان والتعمير", "name_en": "Madinet Masr",
        "sector": "Real Estate", "investing_slug": "madinet-masr-for-housing-and-development"
    },
    {
        "ticker": "POUL", "yahoo": "POUL.CA", "tv": "EGX:POUL",
        "name_ar": "القاهرة للدواجن", "name_en": "Cairo Poultry",
        "sector": "Food", "investing_slug": "cairo-poultry"
    },
    {
        "ticker": "DOMT", "yahoo": "DOMT.CA", "tv": "EGX:DOMT",
        "name_ar": "دومتي - الجودة الغذائية", "name_en": "Domty",
        "sector": "Food & Beverages", "investing_slug": "arab-dairy"
    },
    {
        "ticker": "OLFI", "yahoo": "OLFI.CA", "tv": "EGX:OLFI",
        "name_ar": "أوبر فينانس", "name_en": "Obour Land for Food Industries",
        "sector": "Food", "investing_slug": "obour-land"
    },
    {
        "ticker": "EGTS", "yahoo": "EGTS.CA", "tv": "EGX:EGTS",
        "name_ar": "المصرية للمنتجعات السياحية", "name_en": "Egyptian Resorts",
        "sector": "Tourism", "investing_slug": "egyptian-resorts"
    },
    {
        "ticker": "EMOB", "yahoo": "EMOB.CA", "tv": "EGX:EMOB",
        "name_ar": "موبيكا", "name_en": "Egyptian Modern Education",
        "sector": "Education", "investing_slug": "egyptian-modern-education-systems-sae"
    },
    {
        "ticker": "EGCH2", "yahoo": "EGCH2.CA", "tv": "EGX:EGCH2",
        "name_ar": "إعمار للضيافة", "name_en": "Emaar Hospitality",
        "sector": "Hospitality", "investing_slug": "emaar-misr"
    },
    {
        "ticker": "OBRI", "yahoo": "OBRI.CA", "tv": "EGX:OBRI",
        "name_ar": "أوبيري للمستلزمات الطبية", "name_en": "Obour Industrial Development",
        "sector": "Industrial", "investing_slug": "obour-industrial-development"
    },
    {
        "ticker": "AFMC", "yahoo": "AFMC.CA", "tv": "EGX:AFMC",
        "name_ar": "إيكون - وادي للأسمنت", "name_en": "South Valley Cement",
        "sector": "Cement", "investing_slug": "south-valley-cement"
    },
    {
        "ticker": "DAPH", "yahoo": "DAPH.CA", "tv": "EGX:DAPH",
        "name_ar": "العربية للأدوية", "name_en": "Arab Pharmaceuticals",
        "sector": "Pharmaceuticals", "investing_slug": "arab-pharma-chems"
    },
    {
        "ticker": "PHAR", "yahoo": "PHAR.CA", "tv": "EGX:PHAR",
        "name_ar": "ميديكال يونيون فارماسيوتيكالز", "name_en": "Medical Union Pharmaceuticals",
        "sector": "Pharmaceuticals", "investing_slug": "med-union-pharm"
    },
    {
        "ticker": "PRDC", "yahoo": "PRDC.CA", "tv": "EGX:PRDC",
        "name_ar": "بالم هيلز - الكورنيش", "name_en": "Palm Hills Kattameya",
        "sector": "Real Estate", "investing_slug": "palm-hills-kattameya"
    },
    {
        "ticker": "EGAS", "yahoo": "EGAS.CA", "tv": "EGX:EGAS",
        "name_ar": "ناتجاس", "name_en": "Natural Gas & Mining",
        "sector": "Oil & Gas", "investing_slug": "natural-gas---mining"
    },
    {
        "ticker": "GBCO", "yahoo": "GBCO.CA", "tv": "EGX:GBCO",
        "name_ar": "جي بي كابيتال للخدمات المالية", "name_en": "GB Capital",
        "sector": "Financial Services", "investing_slug": "gb-capital"
    },
    {
        "ticker": "EHDR", "yahoo": "EHDR.CA", "tv": "EGX:EHDR",
        "name_ar": "العربية والإفريقية الدولية للاستثمار", "name_en": "Arab Dairy Products",
        "sector": "Food & Beverages", "investing_slug": "egyptian-german-co-ind-products"
    },
    {
        "ticker": "DEVE", "yahoo": "DEVE.CA", "tv": "EGX:DEVE",
        "name_ar": "ديسكفر للتنمية", "name_en": "Develop. & Engineering Consultants",
        "sector": "Construction", "investing_slug": "development-engineering-consultants"
    },
    {
        "ticker": "BMA", "yahoo": "BMA.CA", "tv": "EGX:BMA",
        "name_ar": "الحرفيين للاستثمار والتنمية العقارية", "name_en": "BMA Heratech",
        "sector": "Real Estate", "investing_slug": "bma"
    },
    {
        "ticker": "CIRA2", "yahoo": "CIRA2.CA", "tv": "EGX:CIRA2",
        "name_ar": "كايرو الثالثة", "name_en": "Cairo Three A",
        "sector": "Education", "investing_slug": "cairo-three-a-poultry"
    },
    {
        "ticker": "PIOH", "yahoo": "PIOH.CA", "tv": "EGX:PIOH",
        "name_ar": "بايونيرز القابضة", "name_en": "Pioneers Holding",
        "sector": "Financial Services", "investing_slug": "pioneers-holding"
    },
    {
        "ticker": "OCDI2", "yahoo": "OCDI2.CA", "tv": "EGX:OCDI2",
        "name_ar": "أوراسكوم القابضة - الفرعية", "name_en": "Orascom Industries",
        "sector": "Industrial", "investing_slug": "orascom-industries"
    },
    {
        "ticker": "ARAB", "yahoo": "ARAB.CA", "tv": "EGX:ARAB",
        "name_ar": "العربية القابضة", "name_en": "Arab Cotton Ginning",
        "sector": "Textiles", "investing_slug": "arab-cotton-ginning"
    },
    {
        "ticker": "CIFI", "yahoo": "CIFI.CA", "tv": "EGX:CIFI",
        "name_ar": "كايرو للزيوت والصابون", "name_en": "Cairo Oils & Soap",
        "sector": "Consumer Goods", "investing_slug": "cairo-oils---soap"
    },
    {
        "ticker": "ELEC", "yahoo": "ELEC.CA", "tv": "EGX:ELEC",
        "name_ar": "الكهرومائية للاستثمار", "name_en": "Electro Cable Egypt",
        "sector": "Electrical Equipment", "investing_slug": "electro-cable-egypt"
    },
    {
        "ticker": "BINV", "yahoo": "BINV.CA", "tv": "EGX:BINV",
        "name_ar": "بنك الاستثمار العربي", "name_en": "Arab Investment Bank",
        "sector": "Banks", "investing_slug": "arab-investment-bank"
    },
    {
        "ticker": "ATLC", "yahoo": "ATLC.CA", "tv": "EGX:ATLC",
        "name_ar": "أطلس للاستثمار العقاري", "name_en": "Atlas Investments",
        "sector": "Real Estate", "investing_slug": "atlas-investment"
    },
    {
        "ticker": "GGCC", "yahoo": "GGCC.CA", "tv": "EGX:GGCC",
        "name_ar": "جلوبال للأسمنت", "name_en": "Egyptian Gulf Bank",
        "sector": "Banks", "investing_slug": "egyptian-gulf-bank"
    },
    {
        "ticker": "CIB", "yahoo": "CIB.CA", "tv": "EGX:CIB",
        "name_ar": "البنك التجاري الدولي", "name_en": "CIB Egypt",
        "sector": "Banks", "investing_slug": "cib-egypt"
    },
    {
        "ticker": "GTHE", "yahoo": "GTHE.CA", "tv": "EGX:GTHE",
        "name_ar": "العاشر من رمضان", "name_en": "Tenth of Ramadan Co",
        "sector": "Industrial", "investing_slug": "tenth-of-ramadan"
    },
    {
        "ticker": "RACT", "yahoo": "RACT.CA", "tv": "EGX:RACT",
        "name_ar": "رواد للاستشارات", "name_en": "Rowad Tourism",
        "sector": "Tourism", "investing_slug": "rowad-tourism"
    },
    {
        "ticker": "GBCO2", "yahoo": "GBCO2.CA", "tv": "EGX:GBCO2",
        "name_ar": "جي بي القابضة", "name_en": "GB Holding",
        "sector": "Investments", "investing_slug": "gb-holding"
    },
    {
        "ticker": "ATQA", "yahoo": "ATQA.CA", "tv": "EGX:ATQA",
        "name_ar": "العتاقة للتنمية", "name_en": "El Ataqa Development",
        "sector": "Industrial", "investing_slug": "el-ataqa"
    },
    {
        "ticker": "IRON", "yahoo": "IRON.CA", "tv": "EGX:IRON",
        "name_ar": "الحديد والصلب المصرية", "name_en": "Egyptian Iron & Steel",
        "sector": "Steel & Iron", "investing_slug": "egyptian-iron-and-steel"
    },
    {
        "ticker": "EFIC", "yahoo": "EFIC.CA", "tv": "EGX:EFIC",
        "name_ar": "كفر الزيات للمبيدات", "name_en": "Kafr Elzayat Pesticides",
        "sector": "Chemicals", "investing_slug": "kafr-el-zayat-pesticides"
    },
    {
        "ticker": "ALCN", "yahoo": "ALCN.CA", "tv": "EGX:ALCN",
        "name_ar": "الإسكندرية للحاويات", "name_en": "Alexandria Containers",
        "sector": "Shipping", "investing_slug": "alexandria-containers"
    },
    {
        "ticker": "UEFM", "yahoo": "UEFM.CA", "tv": "EGX:UEFM",
        "name_ar": "المتحدة للإسكان والتعمير", "name_en": "United Housing & Development",
        "sector": "Real Estate", "investing_slug": "united-housing"
    },
    {
        "ticker": "EXPA", "yahoo": "EXPA.CA", "tv": "EGX:EXPA",
        "name_ar": "اكسبا للتنمية", "name_en": "Export Development Bank",
        "sector": "Banks", "investing_slug": "expa-bank"
    },
    {
        "ticker": "HDBK", "yahoo": "HDBK.CA", "tv": "EGX:HDBK",
        "name_ar": "بنك التعمير والإسكان", "name_en": "Housing & Development Bank",
        "sector": "Banks", "investing_slug": "housing-and-development-bank"
    },
    {
        "ticker": "QNBA", "yahoo": "QNBA.CA", "tv": "EGX:QNBA",
        "name_ar": "بنك قطر الوطني الأهلي", "name_en": "QNB Alahli",
        "sector": "Banks", "investing_slug": "qnb-al-ahli"
    },
    {
        "ticker": "CANA", "yahoo": "CANA.CA", "tv": "EGX:CANA",
        "name_ar": "كنال السويس لتوكيلات الشحن", "name_en": "Canal Shipping Agencies",
        "sector": "Shipping", "investing_slug": "canal-shipping-agencies"
    },
    {
        "ticker": "PACH", "yahoo": "PACH.CA", "tv": "EGX:PACH",
        "name_ar": "باكين للتعبئة والتغليف", "name_en": "Pachin",
        "sector": "Industrial", "investing_slug": "pachin"
    },
    {
        "ticker": "SUGR", "yahoo": "SUGR.CA", "tv": "EGX:SUGR",
        "name_ar": "الدلتا للسكر", "name_en": "Delta Sugar",
        "sector": "Food", "investing_slug": "delta-sugar"
    },
    {
        "ticker": "SCEM", "yahoo": "SCEM.CA", "tv": "EGX:SCEM",
        "name_ar": "السويس للأسمنت", "name_en": "Suez Cement",
        "sector": "Cement", "investing_slug": "suez-cement-company"
    },
    {
        "ticker": "ELSH", "yahoo": "ELSH.CA", "tv": "EGX:ELSH",
        "name_ar": "الشمس للإسكان والتعمير", "name_en": "El Shams Housing",
        "sector": "Real Estate", "investing_slug": "el-shams-housing"
    },
    {
        "ticker": "RMDA", "yahoo": "RMDA.CA", "tv": "EGX:RMDA",
        "name_ar": "راميدا للاستثمار", "name_en": "Rameda Pharma",
        "sector": "Pharmaceuticals", "investing_slug": "rameda"
    },
    {
        "ticker": "ESCC", "yahoo": "ESCC.CA", "tv": "EGX:ESCC",
        "name_ar": "السويس للمنتجات الصلب", "name_en": "Suez Steel Co",
        "sector": "Steel & Iron", "investing_slug": "suez-steel"
    },
    {
        "ticker": "ATQN", "yahoo": "ATQN.CA", "tv": "EGX:ATQN",
        "name_ar": "بنك التنمية الصناعية", "name_en": "Industrial Development Bank",
        "sector": "Banks", "investing_slug": "industrial-development-bank"
    },
    {
        "ticker": "SUCE", "yahoo": "SUCE.CA", "tv": "EGX:SUCE",
        "name_ar": "السكر والصناعات التكاملية", "name_en": "Sugar & Integrated Industries",
        "sector": "Food", "investing_slug": "sugar---integrated-industries"
    },
    {
        "ticker": "PORT", "yahoo": "PORT.CA", "tv": "EGX:PORT",
        "name_ar": "بورتو القابضة", "name_en": "Porto Group Holding",
        "sector": "Tourism", "investing_slug": "porto-group-holding"
    },
    {
        "ticker": "ASCM", "yahoo": "ASCM.CA", "tv": "EGX:ASCM",
        "name_ar": "أسيك للأسمنت", "name_en": "Arabian Cement (Aswan)",
        "sector": "Cement", "investing_slug": "ascom"
    },
    {
        "ticker": "ALCM", "yahoo": "ALCM.CA", "tv": "EGX:ALCM",
        "name_ar": "اللحوم المصرية - بيتي", "name_en": "Egyptian for Tourism Resorts",
        "sector": "Tourism", "investing_slug": "egyptian-tourism"
    },
    {
        "ticker": "EGTL", "yahoo": "EGTL.CA", "tv": "EGX:EGTL",
        "name_ar": "النيل لحليج الأقطان", "name_en": "Nile Cotton Ginning",
        "sector": "Textiles", "investing_slug": "nile-cotton-ginning"
    },
    {
        "ticker": "GMC", "yahoo": "GMC.CA", "tv": "EGX:GMC",
        "name_ar": "جنرال موتورز", "name_en": "General Silos & Storage",
        "sector": "Industrial", "investing_slug": "general-silos"
    },
    {
        "ticker": "MOIL", "yahoo": "MOIL.CA", "tv": "EGX:MOIL",
        "name_ar": "صافي - عناية ميادي", "name_en": "Safi Holding",
        "sector": "Food & Beverages", "investing_slug": "safi"
    },
    {
        "ticker": "OCFI", "yahoo": "OCFI.CA", "tv": "EGX:OCFI",
        "name_ar": "أوراسكوم القابضة المالية", "name_en": "Orascom Financial Holding",
        "sector": "Financial Services", "investing_slug": "orascom-financial-holding"
    },
    {
        "ticker": "CSAG", "yahoo": "CSAG.CA", "tv": "EGX:CSAG",
        "name_ar": "كيرسيرف", "name_en": "Care Service Egypt",
        "sector": "Healthcare", "investing_slug": "care-service-egypt"
    },
    {
        "ticker": "EGFS", "yahoo": "EGFS.CA", "tv": "EGX:EGFS",
        "name_ar": "إجيبت فاير سيرفس", "name_en": "Egypt for Foreign Services",
        "sector": "Services", "investing_slug": "egypt-foreign-services"
    },
    {
        "ticker": "AROP", "yahoo": "AROP.CA", "tv": "EGX:AROP",
        "name_ar": "العربية للاستثمار العقاري", "name_en": "Arabia Investments",
        "sector": "Real Estate", "investing_slug": "arabia-investments"
    },
    {
        "ticker": "MILS", "yahoo": "MILS.CA", "tv": "EGX:MILS",
        "name_ar": "المصرية العقارية", "name_en": "Misr Real Estate Assets",
        "sector": "Real Estate", "investing_slug": "misr-real-estate"
    },
    {
        "ticker": "ASCR", "yahoo": "ASCR.CA", "tv": "EGX:ASCR",
        "name_ar": "أسكوم للتعدين", "name_en": "Ascom Carbonate & Chemical",
        "sector": "Mining", "investing_slug": "ascom-carbonate-and-chemical-manufacturing"
    },
    {
        "ticker": "EGSA", "yahoo": "EGSA.CA", "tv": "EGX:EGSA",
        "name_ar": "السويس للأدوية", "name_en": "Suez Canal Pharmaceutical",
        "sector": "Pharmaceuticals", "investing_slug": "suez-canal-pharmaceutical"
    },
    {
        "ticker": "MOSC", "yahoo": "MOSC.CA", "tv": "EGX:MOSC",
        "name_ar": "موبيكا - الأثاث", "name_en": "Mobica for Furniture",
        "sector": "Consumer Goods", "investing_slug": "mobica"
    },
    {
        "ticker": "AJWA", "yahoo": "AJWA.CA", "tv": "EGX:AJWA",
        "name_ar": "أجوا للصناعات الغذائية", "name_en": "Ajwa for Food Industries",
        "sector": "Food", "investing_slug": "ajwa"
    },
    {
        "ticker": "DCRC", "yahoo": "DCRC.CA", "tv": "EGX:DCRC",
        "name_ar": "ديسكفر للسياحة", "name_en": "Delta Construction & Rebuilding",
        "sector": "Construction", "investing_slug": "delta-construction"
    },
    {
        "ticker": "EXTR", "yahoo": "EXTR.CA", "tv": "EGX:EXTR",
        "name_ar": "إكسترا للصناعات الغذائية", "name_en": "Extracted Oils",
        "sector": "Food", "investing_slug": "extracted-oils"
    },
    {
        "ticker": "INVR", "yahoo": "INVR.CA", "tv": "EGX:INVR",
        "name_ar": "المستثمرون العرب", "name_en": "Arab Investors Union",
        "sector": "Investments", "investing_slug": "arab-investors-union"
    },
    {
        "ticker": "PRDC2", "yahoo": "PRDC2.CA", "tv": "EGX:PRDC2",
        "name_ar": "بريما القابضة", "name_en": "Prima Holding",
        "sector": "Investments", "investing_slug": "prima-holding"
    },
    {
        "ticker": "ZAHRA", "yahoo": "ZAHRA.CA", "tv": "EGX:ZAHRA",
        "name_ar": "الزهراء للزيوت النباتية", "name_en": "Zahraa Maadi",
        "sector": "Food", "investing_slug": "zahraa-maadi"
    },
    {
        "ticker": "ECAP", "yahoo": "ECAP.CA", "tv": "EGX:ECAP",
        "name_ar": "إي كابيتال للاستثمارات", "name_en": "EFG-Hermes Egypt",
        "sector": "Financial Services", "investing_slug": "efg-egypt"
    },
    {
        "ticker": "ENGC", "yahoo": "ENGC.CA", "tv": "EGX:ENGC",
        "name_ar": "الهندسة للصناعات الإلكترونية", "name_en": "Engineering Industries",
        "sector": "Industrial", "investing_slug": "engineering-industries"
    },
    {
        "ticker": "ALCM2", "yahoo": "ALCM2.CA", "tv": "EGX:ALCM2",
        "name_ar": "الإسكندرية للأدوية", "name_en": "Alexandria Pharmaceuticals",
        "sector": "Pharmaceuticals", "investing_slug": "alexandria-pharma"
    },
    {
        "ticker": "ATCG", "yahoo": "ATCG.CA", "tv": "EGX:ATCG",
        "name_ar": "أكوا للمواد الغذائية", "name_en": "Atlas Capital",
        "sector": "Financial Services", "investing_slug": "atlas-capital"
    },
    {
        "ticker": "CICH", "yahoo": "CICH.CA", "tv": "EGX:CICH",
        "name_ar": "إنترناشيونال كومباني للخدمات", "name_en": "International Co for Investment",
        "sector": "Investments", "investing_slug": "international-co-for-investment"
    },
    {
        "ticker": "GMCI", "yahoo": "GMCI.CA", "tv": "EGX:GMCI",
        "name_ar": "السياحة العالمية", "name_en": "Global Tourism",
        "sector": "Tourism", "investing_slug": "global-tourism"
    },
    {
        "ticker": "NCCW", "yahoo": "NCCW.CA", "tv": "EGX:NCCW",
        "name_ar": "النيل للمشروبات", "name_en": "Nile Pharmaceuticals",
        "sector": "Pharmaceuticals", "investing_slug": "nile-pharma"
    },
    {
        "ticker": "ELKA", "yahoo": "ELKA.CA", "tv": "EGX:ELKA",
        "name_ar": "إلكتروستيشن", "name_en": "El Kahera Electronics",
        "sector": "Industrial", "investing_slug": "el-kahera-electronics"
    },
    {
        "ticker": "EGSE", "yahoo": "EGSE.CA", "tv": "EGX:EGSE",
        "name_ar": "السبائك المصرية", "name_en": "Misr National Steel",
        "sector": "Steel & Iron", "investing_slug": "misr-national-steel"
    },
    {
        "ticker": "EFIH2", "yahoo": "EFIH2.CA", "tv": "EGX:EFIH2",
        "name_ar": "إي فاينانس فرعية", "name_en": "E-Finance Subsidiaries",
        "sector": "Technology", "investing_slug": "e-finance-sub"
    },
    {
        "ticker": "PRCL", "yahoo": "PRCL.CA", "tv": "EGX:PRCL",
        "name_ar": "بيرل الاستثمارية", "name_en": "Pearl Investment Group",
        "sector": "Investments", "investing_slug": "pearl-investment"
    },
]


def get_all_tickers():
    """Returns all ticker symbols."""
    return [s["ticker"] for s in EGX_STOCKS]


def get_stock_by_ticker(ticker: str):
    """Find stock by ticker symbol."""
    ticker = ticker.upper().strip()
    for stock in EGX_STOCKS:
        if stock["ticker"].upper() == ticker:
            return stock
    return None


def search_stocks(query: str):
    """Search stocks by Arabic name, English name, or ticker."""
    query = query.strip()
    if not query:
        return []

    query_lower = query.lower()
    results = []

    for stock in EGX_STOCKS:
        if (query_lower in stock["ticker"].lower()
                or query_lower in stock["name_en"].lower()
                or query in stock["name_ar"]):
            results.append(stock)

    return results


def get_egx30_tickers():
    """Returns EGX 30 tickers (first 33 entries in our list)."""
    return [s["ticker"] for s in EGX_STOCKS[:33]]


def get_egx100_tickers():
    """Returns EGX 100 tickers (all entries)."""
    return [s["ticker"] for s in EGX_STOCKS]


def get_sectors():
    """Returns all unique sectors."""
    return sorted(set(s["sector"] for s in EGX_STOCKS))


def get_stocks_by_sector(sector: str):
    """Returns all stocks in a given sector."""
    return [s for s in EGX_STOCKS if s["sector"] == sector]


if __name__ == "__main__":
    print(f"Total stocks in database: {len(EGX_STOCKS)}")
    print(f"Sectors: {get_sectors()}")
