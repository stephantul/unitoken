SPACY_LANGUAGES = [
    "hr",
    "hsb",
    "ro",
    "af",
    "hu",
    "ru",
    "am",
    "hy",
    "sa",
    "ar",
    "id",
    "si",
    "az",
    "is",
    "sk",
    "bg",
    "it",
    "sl",
    "bn",
    "ja",
    "sq",
    "ca",
    "kn",
    "sr",
    "ko",
    "sv",
    "cs",
    "ky",
    "ta",
    "da",
    "la",
    "te",
    "de",
    "lb",
    "th",
    "dsb",
    "ti",
    "el",
    "lg",
    "tl",
    "en",
    "lij",
    "tn",
    "es",
    "lt",
    "et",
    "lv",
    "tr",
    "eu",
    "mk",
    "tt",
    "fa",
    "ml",
    "uk",
    "fi",
    "mr",
    "ur",
    "fr",
    "nb",
    "vi",
    "ga",
    "ne",
    "grc",
    "nl",
    "yo",
    "gu",
    "zh",
    "he",
    "pl",
    "hi",
    "pt",
]

FASTTEXT_LANGUAGES = [
    "af",
    "als",
    "am",
    "an",
    "ar",
    "arz",
    "as",
    "ast",
    "av",
    "az",
    "azb",
    "ba",
    "bar",
    "bcl",
    "be",
    "bg",
    "bh",
    "bn",
    "bo",
    "bpy",
    "br",
    "bs",
    "bxr",
    "ca",
    "cbk",
    "ce",
    "ceb",
    "ckb",
    "co",
    "cs",
    "cv",
    "cy",
    "da",
    "de",
    "diq",
    "dsb",
    "dty",
    "dv",
    "el",
    "eml",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fr",
    "frr",
    "fy",
    "ga",
    "gd",
    "gl",
    "gn",
    "gom",
    "gu",
    "gv",
    "he",
    "hi",
    "hif",
    "hr",
    "hsb",
    "ht",
    "hu",
    "hy",
    "ia",
    "id",
    "ie",
    "ilo",
    "io",
    "is",
    "it",
    "ja",
    "jbo",
    "jv",
    "ka",
    "kk",
    "km",
    "kn",
    "ko",
    "krc",
    "ku",
    "kv",
    "kw",
    "ky",
    "la",
    "lb",
    "lez",
    "li",
    "lmo",
    "lo",
    "lrc",
    "lt",
    "lv",
    "mai",
    "mg",
    "mhr",
    "min",
    "mk",
    "ml",
    "mn",
    "mr",
    "mrj",
    "ms",
    "mt",
    "mwl",
    "my",
    "myv",
    "mzn",
    "nah",
    "nap",
    "nds",
    "ne",
    "new",
    "nl",
    "nn",
    "no",
    "oc",
    "or",
    "os",
    "pa",
    "pam",
    "pfl",
    "pl",
    "pms",
    "pnb",
    "ps",
    "pt",
    "qu",
    "rm",
    "ro",
    "ru",
    "rue",
    "sa",
    "sah",
    "sc",
    "scn",
    "sco",
    "sd",
    "sh",
    "si",
    "sk",
    "sl",
    "so",
    "sq",
    "sr",
    "su",
    "sv",
    "sw",
    "ta",
    "te",
    "tg",
    "th",
    "tk",
    "tl",
    "tr",
    "tt",
    "tyv",
    "ug",
    "uk",
    "ur",
    "uz",
    "vec",
    "vep",
    "vi",
    "vls",
    "vo",
    "wa",
    "war",
    "wuu",
    "xal",
    "xmf",
    "yi",
    "yo",
    "yue",
    "zh",
]

ALLOWED_LANGUAGES = set(SPACY_LANGUAGES) & set(FASTTEXT_LANGUAGES)