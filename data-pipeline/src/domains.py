# Domain → country mappings used in transform.py
#
# Two lookup layers (applied in order):
#   1. TLD_TO_ISO3   — country-code TLDs like .fr .de .ua
#   2. DOMAIN_TO_ISO3 — curated list of major .com/.org/.net outlets
#
# Aggregators (msn.com, yahoo.com, iheart.com, etc.) are intentionally absent —
# they syndicate from everywhere and don't represent a single country's voice.

# ---------------------------------------------------------------------------
# Layer 1: TLD → ISO3
# Covers all standard country-code top-level domains.
# Skipped for generic TLDs: .com .org .net .edu .gov .int
# ---------------------------------------------------------------------------
TLD_TO_ISO3 = {
    "ac": "SHN", "ad": "AND", "ae": "ARE", "af": "AFG", "ag": "ATG",
    "ai": "AIA", "al": "ALB", "am": "ARM", "ao": "AGO", "ar": "ARG",
    "at": "AUT", "au": "AUS", "az": "AZE", "ba": "BIH", "bb": "BRB",
    "bd": "BGD", "be": "BEL", "bf": "BFA", "bg": "BGR", "bh": "BHR",
    "bi": "BDI", "bj": "BEN", "bn": "BRN", "bo": "BOL", "br": "BRA",
    "bs": "BHS", "bt": "BTN", "bw": "BWA", "by": "BLR", "bz": "BLZ",
    "ca": "CAN", "cd": "COD", "cf": "CAF", "cg": "COG", "ch": "CHE",
    "ci": "CIV", "ck": "COK", "cl": "CHL", "cm": "CMR", "cn": "CHN",
    "co": "COL", "cr": "CRI", "cu": "CUB", "cv": "CPV", "cy": "CYP",
    "cz": "CZE", "de": "DEU", "dj": "DJI", "dk": "DNK", "dm": "DMA",
    "do": "DOM", "dz": "DZA", "ec": "ECU", "ee": "EST", "eg": "EGY",
    "er": "ERI", "es": "ESP", "et": "ETH", "fi": "FIN", "fj": "FJI",
    "fk": "FLK", "fm": "FSM", "fo": "FRO", "fr": "FRA", "ga": "GAB",
    "gd": "GRD", "ge": "GEO", "gh": "GHA", "gl": "GRL", "gm": "GMB",
    "gn": "GIN", "gq": "GNQ", "gr": "GRC", "gt": "GTM", "gu": "GUM",
    "gw": "GNB", "gy": "GUY", "hk": "HKG", "hn": "HND", "hr": "HRV",
    "ht": "HTI", "hu": "HUN", "id": "IDN", "ie": "IRL", "il": "ISR",
    "in": "IND", "iq": "IRQ", "ir": "IRN", "is": "ISL", "it": "ITA",
    "jm": "JAM", "jo": "JOR", "jp": "JPN", "ke": "KEN", "kg": "KGZ",
    "kh": "KHM", "ki": "KIR", "km": "COM", "kn": "KNA", "kp": "PRK",
    "kr": "KOR", "kw": "KWT", "ky": "CYM", "kz": "KAZ", "la": "LAO",
    "lb": "LBN", "lc": "LCA", "li": "LIE", "lk": "LKA", "lr": "LBR",
    "ls": "LSO", "lt": "LTU", "lu": "LUX", "lv": "LVA", "ly": "LBY",
    "ma": "MAR", "mc": "MCO", "md": "MDA", "me": "MNE", "mg": "MDG",
    "mh": "MHL", "mk": "MKD", "ml": "MLI", "mm": "MMR", "mn": "MNG",
    "mo": "MAC", "mr": "MRT", "ms": "MSR", "mt": "MLT", "mu": "MUS",
    "mv": "MDV", "mw": "MWI", "mx": "MEX", "my": "MYS", "mz": "MOZ",
    "na": "NAM", "ne": "NER", "ng": "NGA", "ni": "NIC", "nl": "NLD",
    "no": "NOR", "np": "NPL", "nr": "NRU", "nz": "NZL", "om": "OMN",
    "pa": "PAN", "pe": "PER", "pf": "PYF", "pg": "PNG", "ph": "PHL",
    "pk": "PAK", "pl": "POL", "ps": "PSE", "pt": "PRT", "pw": "PLW",
    "py": "PRY", "qa": "QAT", "ro": "ROU", "rs": "SRB", "ru": "RUS",
    "rw": "RWA", "sa": "SAU", "sb": "SLB", "sc": "SYC", "sd": "SDN",
    "se": "SWE", "sg": "SGP", "si": "SVN", "sk": "SVK", "sl": "SLE",
    "sm": "SMR", "sn": "SEN", "so": "SOM", "sr": "SUR", "ss": "SSD",
    "st": "STP", "sv": "SLV", "sy": "SYR", "sz": "SWZ", "td": "TCD",
    "tg": "TGO", "th": "THA", "tj": "TJK", "tl": "TLS", "tm": "TKM",
    "tn": "TUN", "to": "TON", "tr": "TUR", "tt": "TTO", "tv": "TUV",
    "tz": "TZA", "ua": "UKR", "ug": "UGA", "uk": "GBR", "us": "USA",
    "uy": "URY", "uz": "UZB", "va": "VAT", "vc": "VCT", "ve": "VEN",
    "vn": "VNM", "vu": "VUT", "ws": "WSM", "ye": "YEM", "za": "ZAF",
    "zm": "ZMB", "zw": "ZWE",
}

# ---------------------------------------------------------------------------
# Layer 2: curated .com / .org / .net outlets → ISO3
# Covers the top outlets by article volume in GDELT.
# Aggregators (msn, yahoo, iheart, menafn, etc.) are excluded.
# ---------------------------------------------------------------------------
DOMAIN_TO_ISO3 = {

    # United States
    "cnn.com":                   "USA",
    "foxnews.com":               "USA",
    "nytimes.com":               "USA",
    "washingtonpost.com":        "USA",
    "reuters.com":               "USA",
    "apnews.com":                "USA",
    "businessinsider.com":       "USA",
    "marketwatch.com":           "USA",
    "newsweek.com":              "USA",
    "forbes.com":                "USA",
    "bloomberg.com":             "USA",
    "wsj.com":                   "USA",
    "usatoday.com":              "USA",
    "nbcnews.com":               "USA",
    "abcnews.go.com":            "USA",
    "cbsnews.com":               "USA",
    "npr.org":                   "USA",
    "politico.com":              "USA",
    "thehill.com":               "USA",
    "axios.com":                 "USA",
    "vox.com":                   "USA",
    "breitbart.com":             "USA",
    "nypost.com":                "USA",
    "theepochtimes.com":         "USA",
    "vice.com":                  "USA",
    "wired.com":                 "USA",
    "slate.com":                 "USA",
    "motherjones.com":           "USA",
    "theatlantic.com":           "USA",
    "newyorker.com":             "USA",
    "pbs.org":                   "USA",
    "voanews.com":               "USA",
    "rferl.org":                 "USA",
    "military.com":              "USA",
    "defensenews.com":           "USA",
    "foreignpolicy.com":         "USA",
    "washingtontimes.com":       "USA",
    "washingtonexaminer.com":    "USA",
    "oann.com":                  "USA",
    "hotair.com":                "USA",
    "stripes.com":               "USA",
    "mediaite.com":              "USA",
    "cnsnews.com":               "USA",
    "startribune.com":           "USA",
    "sandiegouniontribune.com":  "USA",
    "seattlepi.com":             "USA",
    "sfgate.com":                "USA",
    "chron.com":                 "USA",
    "stltoday.com":              "USA",
    "buffalonews.com":           "USA",
    "omaha.com":                 "USA",
    "go.com":                    "USA",
    "gazette.com":               "USA",
    "missoulian.com":            "USA",
    "smdailyjournal.com":        "USA",
    "mynorthwest.com":           "USA",
    "nbclosangeles.com":         "USA",
    "nbcdfw.com":                "USA",
    "nbcconnecticut.com":        "USA",
    "nbcmiami.com":              "USA",
    "nbcnewyork.com":            "USA",
    "nbcsandiego.com":           "USA",
    "nbcphiladelphia.com":       "USA",
    "zerohedge.com":             "USA",
    "bozemandailychronicle.com": "USA",
    "caledonianrecord.com":      "USA",
    "tucson.com":                "USA",
    "kelo.com":                  "USA",
    "ktvz.com":                  "USA",
    "kvia.com":                  "USA",
    "kstp.com":                  "USA",
    "krdo.com":                  "USA",
    "wbal.com":                  "USA",
    "wtmj.com":                  "USA",
    "wfmz.com":                  "USA",
    "goskagit.com":              "USA",
    "ifiberone.com":             "USA",
    "siouxcityjournal.com":      "USA",
    "news-gazette.com":          "USA",
    "kdhnews.com":               "USA",
    "swoknews.com":              "USA",
    "ctpost.com":                "USA",
    "nhregister.com":            "USA",
    "channel3000.com":           "USA",
    "localnews8.com":            "USA",
    "abc17news.com":             "USA",
    "kwbu.org":                  "USA",
    "wbaa.org":                  "USA",
    "kasu.org":                  "USA",
    "wsau.com":                  "USA",

    # United Kingdom
    "theguardian.com":           "GBR",
    "bbc.com":                   "GBR",
    "ft.com":                    "GBR",
    "sky.com":                   "GBR",
    "economist.com":             "GBR",
    "telegraph.co.uk":           "GBR",
    "thetimes.co.uk":            "GBR",
    "independent.co.uk":         "GBR",
    "dailymail.co.uk":           "GBR",
    "express.co.uk":             "GBR",
    "mirror.co.uk":              "GBR",
    "thesun.co.uk":              "GBR",
    "dunfermlinepress.com":      "GBR",
    "britainnews.net":           "GBR",

    # Russia
    "rt.com":                    "RUS",
    "sputniknews.com":           "RUS",
    "russiaherald.com":          "RUS",
    "tass.com":                  "RUS",
    "themoscowtimes.com":        "RUS",
    "interfax.com":              "RUS",

    # Ukraine
    "korrespondent.net":         "UKR",
    "unian.net":                 "UKR",
    "kyivpost.com":              "UKR",
    "ukrinform.net":             "UKR",
    "glavred.info":              "UKR",
    "obozrevatel.com":           "UKR",
    "pravda.com.ua":             "UKR",
    "gordonua.com":              "UKR",
    "ukrainianwall.com":         "UKR",
    "liga.net":                  "UKR",
    "vesti-ua.net":              "UKR",

    # Germany
    "dw.com":                    "DEU",
    "faz.net":                   "DEU",
    "handelsblatt.com":          "DEU",
    "zeit.de":                   "DEU",
    "sueddeutsche.de":           "DEU",

    # France
    "france24.com":              "FRA",
    "bfmtv.com":                 "FRA",
    "euronews.com":              "FRA",
    "la-croix.com":              "FRA",
    "varmatin.com":              "FRA",
    "nicematin.com":             "FRA",
    "laprovence.com":            "FRA",
    "marketscreener.com":        "FRA",

    # Belgium
    "politico.eu":               "BEL",
    "lavenir.net":               "BEL",

    # Spain
    "efe.com":                   "ESP",
    "elpuntavui.cat":            "ESP",

    # Italy
    "adnkronos.com":             "ITA",
    "ansa.it":                   "ITA",
    "ilroma.net":                "ITA",
    "dagospia.com":              "ITA",

    # Poland
    "tvp.info":                  "POL",

    # Sweden
    "tt.com":                    "SWE",

    # Ireland
    "irishtimes.com":            "IRL",
    "rte.ie":                    "IRL",
    "impartialreporter.com":     "IRL",

    # Serbia
    "naslovi.net":               "SRB",

    # Kosovo
    "telegrafi.com":             "XKX",

    # Lebanon
    "naharnet.com":              "LBN",
    "lebanese-forces.com":       "LBN",

    # Turkey
    "dailysabah.com":            "TUR",
    "trtworld.com":              "TUR",
    "haberler.com":              "TUR",
    "sondakika.com":             "TUR",
    "hurriyet.com.tr":           "TUR",

    # India
    "indiatimes.com":            "IND",
    "business-standard.com":     "IND",
    "ndtv.com":                  "IND",
    "jagran.com":                "IND",
    "thehindu.com":              "IND",
    "hindustantimes.com":        "IND",
    "india.com":                 "IND",
    "firstpost.com":             "IND",
    "wionews.com":               "IND",
    "zeenews.india.com":         "IND",
    "tribuneindia.com":          "IND",
    "deccanherald.com":          "IND",
    "livehindustan.com":         "IND",
    "sakshi.com":                "IND",
    "prajavani.net":             "IND",
    "indiagazette.com":          "IND",
    "latestly.com":              "IND",
    "telegraphindia.com":        "IND",
    "indiatvnews.com":           "IND",
    "bhaskar.com":               "IND",
    "prabhasakshi.com":          "IND",
    "dnaindia.com":              "IND",

    # Pakistan
    "dawn.com":                  "PAK",
    "geo.tv":                    "PAK",
    "thenews.com.pk":            "PAK",

    # Israel
    "timesofisrael.com":         "ISR",
    "haaretz.com":               "ISR",
    "jpost.com":                 "ISR",
    "ynetnews.com":              "ISR",

    # Iran
    "presstv.ir":                "IRN",
    "tehrantimes.com":           "IRN",

    # Saudi Arabia
    "aawsat.com":                "SAU",

    # UAE
    "khaleejtimes.com":          "ARE",
    "gulfnews.com":              "ARE",

    # Qatar
    "aljazeera.com":             "QAT",

    # China
    "chinadaily.com.cn":         "CHN",
    "globaltimes.cn":            "CHN",
    "xinhuanet.com":             "CHN",

    # Japan
    "japantimes.co.jp":          "JPN",
    "nhk.or.jp":                 "JPN",

    # South Korea
    "koreaherald.com":           "KOR",
    "koreatimes.co.kr":          "KOR",

    # Singapore
    "straitstimes.com":          "SGP",

    # Malaysia
    "malaymail.com":             "MYS",

    # Indonesia
    "pikiran-rakyat.com":        "IDN",
    "kompas.com":                "IDN",
    "detik.com":                 "IDN",

    # Vietnam
    "baomoi.com":                "VNM",
    "vnexpress.net":             "VNM",
    "vietgiaitri.com":           "VNM",

    # Cambodia
    "cambodiantimes.com":        "KHM",

    # Bangladesh
    "bdnews24.com":              "BGD",
    "thedailystar.net":          "BGD",

    # Australia
    "abc.net.au":                "AUS",
    "smh.com.au":                "AUS",
    "theaustralian.com.au":      "AUS",
    "afr.com":                   "AUS",
    "theconversation.com":       "AUS",

    # Canada
    "globalnews.ca":             "CAN",
    "nationalpost.com":          "CAN",
    "cbc.ca":                    "CAN",
    "digitaljournal.com":        "CAN",
    "journaldemontreal.com":     "CAN",

    # Brazil
    "globo.com":                 "BRA",
    "uol.com.br":                "BRA",
    "folha.uol.com.br":          "BRA",
    "brasil247.com":             "BRA",

    # Argentina
    "taringa.net":               "ARG",
    "infobae.com":               "ARG",
    "clarin.com":                "ARG",

    # Nigeria
    "premiumtimesng.com":        "NGA",
    "vanguardngr.com":           "NGA",
    "thisdaylive.com":           "NGA",

    # Kenya
    "nation.africa":             "KEN",
    "standardmedia.co.ke":       "KEN",

    # South Africa
    "news24.com":                "ZAF",
    "dailymaverick.co.za":       "ZAF",

    # Jamaica
    "jamaicaobserver.com":       "JAM",

    # Portugal
    "noticiasaominuto.com":      "PRT",
    "publico.pt":                "PRT",

    # Philippines
    "inquirer.net":              "PHL",
    "rappler.com":               "PHL",
}

# Generic TLDs — TLD alone tells us nothing about country
TLD_GENERIC = {"com", "org", "net", "edu", "gov", "int"}
