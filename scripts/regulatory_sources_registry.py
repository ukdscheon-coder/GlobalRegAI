"""
GlobalRegAI — 전 세계 규정 데이터 소스 레지스트리
모든 무료 공개 규정 소스의 URL, API, 설명을 정의합니다.
"""

REGULATORY_SOURCES = {

    # ══════════════════════════════════════════════════════════
    # 1. 미국 FDA (US Food and Drug Administration)
    # ══════════════════════════════════════════════════════════
    "FDA": {
        "agency": "FDA",
        "country": "US",
        "language": "en",
        "apis": {
            "drug_enforcement":       "https://api.fda.gov/drug/enforcement.json",
            "drug_event":             "https://api.fda.gov/drug/event.json",
            "drug_label":             "https://api.fda.gov/drug/label.json",
            "device_510k":            "https://api.fda.gov/device/510k.json",
            "device_recall":          "https://api.fda.gov/device/recall.json",
            "device_adverse_event":   "https://api.fda.gov/device/event.json",
            "device_classification":  "https://api.fda.gov/device/classification.json",
            "device_pma":             "https://api.fda.gov/device/pma.json",
            "food_enforcement":       "https://api.fda.gov/food/enforcement.json",
            "food_event":             "https://api.fda.gov/food/event.json",
        },
        "guidance_pages": [
            "https://www.fda.gov/regulatory-information/search-fda-guidance-documents",
            "https://www.fda.gov/medical-devices/guidance-documents-medical-devices-and-radiation-emitting-products",
            "https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs",
            "https://www.fda.gov/cosmetics/cosmetics-laws-regulations",
            "https://www.fda.gov/food/guidance-documents-regulatory-information-topic",
        ],
        "key_regulations": {
            "21_CFR_820": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820",
            "21_CFR_211": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",
            "21_CFR_110": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-110",
            "21_CFR_700": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-G/part-700",
        },
        "pdf_guidance": [
            # Medical Device
            ("Design Controls Guidance", "https://www.fda.gov/media/116573/download"),
            ("Process Validation Guidance", "https://www.fda.gov/media/71021/download"),
            ("Software Validation Guidance", "https://www.fda.gov/media/73141/download"),
            ("Cybersecurity Guidance 2023", "https://www.fda.gov/media/119933/download"),
            ("De Novo Guidance", "https://www.fda.gov/media/87987/download"),
            ("510k Refuse to Accept", "https://www.fda.gov/media/119933/download"),
            # Pharmaceutical
            ("Q7A GMP API", "https://www.fda.gov/media/71518/download"),
            ("Bioanalytical Method Validation", "https://www.fda.gov/media/70858/download"),
            ("Pharmaceutical cGMP Initiative", "https://www.fda.gov/media/71012/download"),
        ],
        "rss_feeds": [
            "https://www.fda.gov/feeds/fda-rss.xml",
            "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/medical-devices/rss.xml",
            "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/drugs/rss.xml",
            "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/food/rss.xml",
        ],
    },

    # ══════════════════════════════════════════════════════════
    # 2. 미국 연방 법령 (eCFR - Electronic Code of Federal Regulations)
    # ══════════════════════════════════════════════════════════
    "eCFR": {
        "agency": "eCFR",
        "country": "US",
        "language": "en",
        "base_api": "https://www.ecfr.gov/api/versioner/v1",
        "key_titles": {
            "Title 21 - Food and Drugs": "https://www.ecfr.gov/current/title-21",
            "Title 40 - Protection of Environment": "https://www.ecfr.gov/current/title-40",
            "Title 29 - Labor (OSHA)": "https://www.ecfr.gov/current/title-29",
            "Title 47 - Telecommunications (FCC)": "https://www.ecfr.gov/current/title-47",
        },
        "medical_device_parts": [
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-800",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-801",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-806",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-807",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-814",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-830",
        ],
        "pharma_parts": [
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-210",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-312",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-314",
        ],
        "food_parts": [
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-110",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-117",
        ],
    },

    # ══════════════════════════════════════════════════════════
    # 3. EU 규정 (EUR-Lex + EMA + EC Health)
    # ══════════════════════════════════════════════════════════
    "EMA": {
        "agency": "EMA",
        "country": "EU",
        "language": "en",
        "guidelines_pages": [
            "https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline",
            "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/scientific-guidelines",
            "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/compliance/good-manufacturing-practice",
        ],
        "key_documents": {
            "GMP_Part1":     "https://health.ec.europa.eu/system/files/2022-09/2022_gmp-guidelines_annex1_en_0.pdf",
            "GMP_Part2":     "https://health.ec.europa.eu/system/files/2022-09/vol4_an11_en_0.pdf",
            "GMP_Annex11":   "https://health.ec.europa.eu/system/files/2022-09/vol4_an11_en_0.pdf",
            "MDR_2017_745":  "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0745",
            "IVDR_2017_746": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0746",
        },
        "eurlex_api": "https://eur-lex.europa.eu/eurlex-ws",
        "cellar_sparql": "https://publications.europa.eu/webapi/rdf/sparql",
        "rss_feeds": [
            "https://www.ema.europa.eu/en/rss/press-releases",
            "https://www.ema.europa.eu/en/rss/human-medicines",
        ],
    },

    # ══════════════════════════════════════════════════════════
    # 4. WHO (World Health Organization)
    # ══════════════════════════════════════════════════════════
    "WHO": {
        "agency": "WHO",
        "country": "Global",
        "language": "en",
        "guidelines_pages": [
            "https://www.who.int/publications/i/item/978924154969-5",
            "https://www.who.int/teams/health-product-and-policy-standards/standards-and-specifications/norms-and-standards-for-pharmaceuticals",
        ],
        "key_pdfs": [
            ("WHO GMP Pharmaceuticals", "https://www.who.int/docs/default-source/medicines/norms-and-standards/guidelines/production/trs986-annex2-gmp-pharmaceuticals.pdf"),
            ("WHO GMP Medical Devices", "https://iris.who.int/bitstream/handle/10665/44697/9789241501736_eng.pdf"),
            ("WHO Pharmacovigilance Guidelines", "https://www.who.int/publications/i/item/who-pharm-s-nss-2020-2"),
            ("WHO Codex HACCP", "https://www.fao.org/fao-who-codexalimentarius/sh-proxy/en/?lnk=1&url=https%3A%2F%2Fworkspace.fao.org%2Fsites%2Fcodex%2FStandards%2FCXC%201-1969%2FCXC_001e.pdf"),
        ],
        "iris_api": "https://iris.who.int/rest/handle",
    },

    # ══════════════════════════════════════════════════════════
    # 5. ICH (International Council for Harmonisation)
    # ══════════════════════════════════════════════════════════
    "ICH": {
        "agency": "ICH",
        "country": "Global",
        "language": "en",
        "guidelines_page": "https://www.ich.org/page/quality-guidelines",
        "key_guidelines": {
            "Q1A": "https://database.ich.org/sites/default/files/Q1A%28R2%29%20Guideline.pdf",
            "Q2R1": "https://database.ich.org/sites/default/files/Q2%28R1%29%20Guideline.pdf",
            "Q3A": "https://database.ich.org/sites/default/files/ICH_Q3A%28R2%29_Guideline_Step4_2006_10.pdf",
            "Q6A": "https://database.ich.org/sites/default/files/Q6A%20Guideline.pdf",
            "Q7":  "https://database.ich.org/sites/default/files/Q7%20Guideline.pdf",
            "Q8R2": "https://database.ich.org/sites/default/files/Q8%28R2%29%20Guideline.pdf",
            "Q9R1": "https://database.ich.org/sites/default/files/Q9-R1-Step4-Guideline_2023_0126.pdf",
            "Q10": "https://database.ich.org/sites/default/files/Q10%20Guideline.pdf",
            "Q11": "https://database.ich.org/sites/default/files/Q11%20Guideline.pdf",
            "Q12": "https://database.ich.org/sites/default/files/Q12_Guideline_Step4_2019_1119.pdf",
            "E6R3": "https://database.ich.org/sites/default/files/ICH_E6(R3)_GuideLine_Step4_2024_0519.pdf",
        },
    },

    # ══════════════════════════════════════════════════════════
    # 6. PIC/S (Pharmaceutical Inspection Co-operation Scheme)
    # ══════════════════════════════════════════════════════════
    "PICS": {
        "agency": "PIC/S",
        "country": "Global",
        "language": "en",
        "guidelines_page": "https://picscheme.org/en/publications",
        "key_guides": {
            "GMP_PE009": "https://picscheme.org/docview/4218",
            "GMP_Annex1": "https://picscheme.org/docview/4220",
            "GMP_Annex11": "https://picscheme.org/docview/4227",
            "GMP_Data_Integrity": "https://picscheme.org/docview/4234",
        },
    },

    # ══════════════════════════════════════════════════════════
    # 7. 한국 MFDS (식품의약품안전처)
    # ══════════════════════════════════════════════════════════
    "MFDS": {
        "agency": "MFDS",
        "country": "Korea",
        "language": "ko",
        "main_site": "https://www.mfds.go.kr",
        "english_site": "https://www.mfds.go.kr/eng",
        "law_pages": [
            "https://www.mfds.go.kr/brd/m_74/list.do",   # 의료기기 관련 법령
            "https://www.mfds.go.kr/brd/m_75/list.do",   # 의약품 관련 법령
            "https://www.mfds.go.kr/brd/m_76/list.do",   # 화장품 관련 법령
            "https://www.mfds.go.kr/brd/m_77/list.do",   # 식품 관련 법령
        ],
        "guidance_pages": [
            "https://www.mfds.go.kr/brd/m_218/list.do",  # 의료기기 가이드라인
            "https://www.mfds.go.kr/brd/m_217/list.do",  # 의약품 가이드라인
        ],
        "english_pages": [
            "https://www.mfds.go.kr/eng/brd/m_60/list.do",
        ],
    },

    # ══════════════════════════════════════════════════════════
    # 8. 일본 PMDA (医薬品医療機器総合機構)
    # ══════════════════════════════════════════════════════════
    "PMDA": {
        "agency": "PMDA",
        "country": "Japan",
        "language": "ja",
        "english_site": "https://www.pmda.go.jp/english/index.html",
        "guidance_pages": [
            "https://www.pmda.go.jp/english/rs-sb-std/standards-development/0001.html",
            "https://www.pmda.go.jp/english/review-services/reviews/approved-information/md/0001.html",
        ],
        "key_pages": [
            "https://www.pmda.go.jp/english/rs-sb-std/standards-development/ig/0001.html",
        ],
    },

    # ══════════════════════════════════════════════════════════
    # 9. 중국 NMPA (国家药品监督管理局)
    # ══════════════════════════════════════════════════════════
    "NMPA": {
        "agency": "NMPA",
        "country": "China",
        "language": "zh",
        "main_site": "https://www.nmpa.gov.cn",
        "english_site": "https://english.nmpa.gov.cn",
        "key_pages": [
            "https://english.nmpa.gov.cn/2019-07/03/c_399496.htm",
            "https://www.nmpa.gov.cn/xxgk/fgwj/flxzhfg/index.html",
        ],
    },

    # ══════════════════════════════════════════════════════════
    # 10. 스페인 AEMPS + 중남미 기관
    # ══════════════════════════════════════════════════════════
    "AEMPS": {
        "agency": "AEMPS",
        "country": "Spain",
        "language": "es",
        "main_site": "https://www.aemps.gob.es",
        "guidelines": [
            "https://www.aemps.gob.es/medicamentosUsoHumano/informesPublicos/home.htm",
            "https://www.aemps.gob.es/productosSanitarios/home.htm",
        ],
    },
    "COFEPRIS": {
        "agency": "COFEPRIS",
        "country": "Mexico",
        "language": "es",
        "main_site": "https://www.gob.mx/cofepris",
        "regulations": [
            "https://www.gob.mx/cofepris/documentos/normas-oficiales-mexicanas",
        ],
    },
    "ANMAT": {
        "agency": "ANMAT",
        "country": "Argentina",
        "language": "es",
        "main_site": "https://www.argentina.gob.ar/anmat",
        "dispositions": "https://www.argentina.gob.ar/anmat/disposiciones",
    },
    "INVIMA": {
        "agency": "INVIMA",
        "country": "Colombia",
        "language": "es",
        "main_site": "https://www.invima.gov.co",
        "normativa": "https://www.invima.gov.co/normativa",
    },

    # ══════════════════════════════════════════════════════════
    # 11. ISO / IEC 표준 (공개 요약)
    # ══════════════════════════════════════════════════════════
    "ISO": {
        "agency": "ISO",
        "country": "Global",
        "language": "en",
        "standards_pages": {
            "ISO_13485": "https://www.iso.org/standard/59752.html",
            "ISO_14971": "https://www.iso.org/standard/72704.html",
            "ISO_9001":  "https://www.iso.org/standard/62085.html",
            "ISO_14644": "https://www.iso.org/standard/53394.html",  # Cleanrooms
            "ISO_11135": "https://www.iso.org/standard/56137.html",  # Sterilization (EO)
            "ISO_11137": "https://www.iso.org/standard/62925.html",  # Sterilization (Radiation)
            "ISO_10993": "https://www.iso.org/standard/68936.html",  # Biocompatibility
            "IEC_62304": "https://www.iso.org/standard/38421.html",  # Med Device Software
            "IEC_60601": "https://www.iso.org/standard/41986.html",  # Electrical Safety
            "IEC_61010": "https://www.iso.org/standard/62951.html",  # Lab Equipment Safety
            "ISO_22000": "https://www.iso.org/standard/65464.html",  # Food Safety
            "ISO_45001": "https://www.iso.org/standard/63787.html",  # OH&S
        },
    },

    # ══════════════════════════════════════════════════════════
    # 12. 규정 커뮤니티 & 포럼
    # ══════════════════════════════════════════════════════════
    "COMMUNITIES": {
        "RAPS_Regulatory_Focus": {
            "url": "https://www.raps.org/news-and-articles",
            "rss": "https://www.raps.org/rss/news",
            "topics": ["medical device", "pharmaceutical", "regulatory news"],
            "language": "en",
            "free": True,
        },
        "Elsmar_Cove": {
            "url": "https://elsmar.com/elsmarqualityforum/",
            "forums": [
                "https://elsmar.com/elsmarqualityforum/forums/21-cfr-820-qsr-qmsr.128/",
                "https://elsmar.com/elsmarqualityforum/forums/iso-13485.78/",
                "https://elsmar.com/elsmarqualityforum/forums/eu-mdr.145/",
            ],
            "language": "en",
            "free": True,
        },
        "Reddit_RegAffairs": {
            "url": "https://www.reddit.com/r/regulatoryaffairs",
            "api": "https://www.reddit.com/r/regulatoryaffairs/top.json?limit=100",
            "language": "en",
            "free": True,
        },
        "Reddit_MedDevice": {
            "url": "https://www.reddit.com/r/medicaldevices",
            "api": "https://www.reddit.com/r/medicaldevices/top.json?limit=100",
            "language": "en",
            "free": True,
        },
        "Reddit_Pharma": {
            "url": "https://www.reddit.com/r/pharma",
            "api": "https://www.reddit.com/r/pharma/top.json?limit=100",
            "language": "en",
            "free": True,
        },
        "PubMed": {
            "url": "https://pubmed.ncbi.nlm.nih.gov",
            "api": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            "language": "en",
            "free": True,
            "queries": [
                "GMP compliance medical device",
                "regulatory submission pharmaceutical",
                "ISO 13485 quality management",
                "FDA 510k approval process",
                "clinical evaluation medical device",
            ],
        },
        "ISPE": {
            "url": "https://ispe.org",
            "news": "https://ispe.org/pharmaceutical-engineering/online-articles",
            "language": "en",
            "free": True,
        },
    },

    # ══════════════════════════════════════════════════════════
    # 13. 전기/화학 규정
    # ══════════════════════════════════════════════════════════
    "ELECTRICAL": {
        "IEC_TC62": {
            "description": "IEC Technical Committee 62 - Electrical equipment for medical use",
            "url": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:1216",
            "key_standards": ["IEC 60601-1", "IEC 60601-1-2 (EMC)", "IEC 60601-1-6 (Usability)", "IEC 62304", "IEC 62366"],
        },
        "CE_LVD": {
            "description": "EU Low Voltage Directive 2014/35/EU",
            "url": "https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/low-voltage-directive_en",
        },
        "CE_EMC": {
            "description": "EU EMC Directive 2014/30/EU",
            "url": "https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/emc-directive_en",
        },
        "FCC": {
            "description": "US Federal Communications Commission - Electronic emissions",
            "api": "https://www.ecfr.gov/current/title-47",
            "url": "https://www.fcc.gov/engineering-technology/laboratory-division/general/equipment-authorization",
        },
        "UL": {
            "description": "UL Standards (Underwriters Laboratories)",
            "url": "https://standardscatalog.ul.com",
        },
        "KC_Mark": {
            "description": "Korea Certification (KC마크) - National Radio Research Agency",
            "url": "https://www.rra.go.kr/en/",
        },
    },

    # ══════════════════════════════════════════════════════════
    # 14. 화학물질 규정 (REACH, GHS, OSHA)
    # ══════════════════════════════════════════════════════════
    "CHEMICAL": {
        "REACH": {
            "description": "EU REACH Regulation (EC) 1907/2006",
            "echa_api": "https://echa.europa.eu/information-on-chemicals",
            "substance_search": "https://echa.europa.eu/information-on-chemicals/ec-inventory",
            "url": "https://echa.europa.eu/regulations/reach/understanding-reach",
        },
        "GHS": {
            "description": "Globally Harmonized System of Classification and Labelling",
            "url": "https://unece.org/trans/danger/publi/ghs/ghs_rev10/10files_e.html",
        },
        "OSHA": {
            "description": "US OSHA Hazard Communication Standard (HCS)",
            "url": "https://www.osha.gov/hazcom",
            "api": "https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/subpart-Z",
        },
        "RoHS": {
            "description": "EU RoHS Directive 2011/65/EU - Restriction of Hazardous Substances",
            "url": "https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/rohs-directive_en",
        },
        "TSCA": {
            "description": "US Toxic Substances Control Act",
            "url": "https://www.epa.gov/tsca-inventory",
            "api": "https://cdxapps.epa.gov/oms-substance-registry-services/rest-api",
        },
        "CLP": {
            "description": "EU CLP Regulation (EC) 1272/2008 - Classification, Labelling, Packaging",
            "url": "https://echa.europa.eu/regulations/clp/understanding-clp",
        },
        "KOSHER_HALAL": {
            "description": "Food ingredient certification databases",
            "url": "https://www.certifiedkosher.com",
        },
        "K_CHEMICALS": {
            "description": "Korea Chemical Substance Management (화학물질관리법)",
            "url": "https://kreach.me.go.kr/chm/main.do",
            "english": "https://www.nier.go.kr/NIER/EngIndexMain.do",
        },
    },

    # ══════════════════════════════════════════════════════════
    # 15. 식품 규정 전문 기관
    # ══════════════════════════════════════════════════════════
    "FOOD": {
        "Codex_Alimentarius": {
            "description": "국제식품규격위원회 - FAO/WHO 공동",
            "url": "https://www.fao.org/fao-who-codexalimentarius",
            "standards_api": "https://www.fao.org/fao-who-codexalimentarius/codex-texts/codes-of-practice/en/",
        },
        "EFSA": {
            "description": "European Food Safety Authority",
            "url": "https://www.efsa.europa.eu",
            "open_data": "https://www.efsa.europa.eu/en/science/open-efsa",
            "api": "https://open.efsa.europa.eu/data",
        },
        "FSANZ": {
            "description": "Food Standards Australia New Zealand",
            "url": "https://www.foodstandards.gov.au",
        },
        "MFDS_Food": {
            "description": "한국 식품 규정 (MFDS)",
            "url": "https://www.foodsafetykorea.go.kr",
            "english": "https://www.foodsafetykorea.go.kr/portal/board/boardList.do",
        },
    },

    # ══════════════════════════════════════════════════════════
    # 16. GMP 전문 정보 사이트
    # ══════════════════════════════════════════════════════════
    "GMP_RESOURCES": {
        "ECA_Academy": {
            "description": "European Compliance Academy - GMP Guidelines Database",
            "url": "https://www.gmp-compliance.org/guidelines",
            "free_resources": "https://www.gmp-compliance.org/guidelines/gmp-guideline",
        },
        "ISPE_GAMP": {
            "description": "ISPE GAMP 5 - Software Validation",
            "url": "https://ispe.org/initiatives/regulatory/gamp",
        },
        "GMP_Review": {
            "description": "GMP Review - Free GMP articles",
            "url": "https://www.gmpreview.com",
        },
        "Pharmaceutical_Online": {
            "description": "Pharmaceutical manufacturing articles",
            "url": "https://www.pharmaceuticalonline.com/regulatory",
        },
        "IVT_Network": {
            "description": "IVT Network - Pharma compliance",
            "url": "https://www.ivtnetwork.com",
        },
    },

    # ══════════════════════════════════════════════════════════
    # 17. 호주, 캐나다, 영국
    # ══════════════════════════════════════════════════════════
    "OTHER_AGENCIES": {
        "TGA": {
            "agency": "TGA",
            "country": "Australia",
            "language": "en",
            "url": "https://www.tga.gov.au",
            "guidance": "https://www.tga.gov.au/resources/publications",
            "database": "https://www.tga.gov.au/resources/artg",
        },
        "Health_Canada": {
            "agency": "Health Canada",
            "country": "Canada",
            "language": "en",
            "url": "https://www.canada.ca/en/health-canada.html",
            "guidance": "https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/applications-submissions/guidance-documents.html",
        },
        "MHRA": {
            "agency": "MHRA",
            "country": "UK",
            "language": "en",
            "url": "https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency",
            "guidance": "https://www.gov.uk/guidance/medical-devices-eu-regulations-for-mdr-and-ivdr",
        },
        "ANVISA": {
            "agency": "ANVISA",
            "country": "Brazil",
            "language": "pt",
            "url": "https://www.gov.br/anvisa/pt-br",
            "english": "https://www.gov.br/anvisa/en",
        },
        "IMDRF": {
            "description": "International Medical Device Regulators Forum",
            "url": "https://www.imdrf.org",
            "documents": "https://www.imdrf.org/documents",
        },
    },
}

if __name__ == "__main__":
    total = sum(
        len(v.get("apis", {})) + len(v.get("key_pdfs", [])) + len(v.get("key_guidelines", {}))
        for v in REGULATORY_SOURCES.values()
        if isinstance(v, dict)
    )
    print(f"Total registered sources: {len(REGULATORY_SOURCES)} agencies")
    print(f"Total API endpoints + documents: {total}+")
