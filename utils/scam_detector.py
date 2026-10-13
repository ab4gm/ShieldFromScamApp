# ==============================================================
# utils/scam_detector.py
# The analysis engine of ShieldFromScamApp.
#
# How it works (no API key needed!):
#   - Layer 1: High-confidence single phrases (classic scam openers)
#   - Layer 2: Regex patterns (flexible number/amount detection)
#   - Layer 3: Context combinations — multiple weak signals that
#              together indicate a scam even if each word alone
#              is innocent
#
# v6 scoring improvements:
#   - Delivery scam: "usps/fedex/ups" + suspicious link + fee now
#     fires a dedicated HIGH-weight rule (was only weight 3 combo).
#   - Bank phishing: impersonation + identity confirm + suspicious
#     link fires a new dedicated rule at weight 5.
#   - Job/employment fee scam: "selected" + job keywords + fee +
#     payment method fires a new rule at weight 5.
#   - MAX_WEIGHT raised to 24 so that 3 strong signals = ~65+
#     (Likely Scam) while 1 strong signal = ~17 (Slightly Suspicious).
#   - "account suspended" / "verify your account" weights raised
#     to 3 so bank phishing phrases contribute more individually.
#   - "you have been selected" raised to weight 4 (was 3).
#   - Verdict thresholds unchanged: <15 safe, <35 slightly,
#     <60 suspicious, 60+ scam.
# ==============================================================

import re

# ──────────────────────────────────────────────────────────────────────────────
# LAYER 1 — Plain-string patterns
# weight: 1=mild, 2=moderate, 3=high, 4=very high
# ──────────────────────────────────────────────────────────────────────────────
SCAM_PATTERNS = [
    # Self-identification
    {"phrase": "scammer",                        "weight": 4, "reason": "Message explicitly mentions a scammer"},
    {"phrase": "i am a scammer",                 "weight": 4, "reason": "Direct self-identification as a scammer"},
    {"phrase": "i'm a scammer",                  "weight": 4, "reason": "Direct self-identification as a scammer"},

    # Urgency / Pressure
    {"phrase": "act now",                        "weight": 2, "reason": "Creates false urgency to rush you into a decision without thinking"},
    {"phrase": "limited time offer",             "weight": 2, "reason": "High-pressure tactic — scammers want you to act before you can verify"},
    {"phrase": "limited time",                   "weight": 1, "reason": "Urgency language used to prevent careful thinking"},
    {"phrase": "expires today",                  "weight": 2, "reason": "Fake deadline pressure — real companies give proper advance notice"},
    {"phrase": "urgent",                         "weight": 1, "reason": "False urgency is a top scam warning sign"},
    {"phrase": "respond immediately",            "weight": 2, "reason": "Demands instant action to prevent you from verifying the sender"},
    {"phrase": "final notice",                   "weight": 2, "reason": "Fake 'last warning' notices are a classic scam pattern"},
    {"phrase": "last chance",                    "weight": 2, "reason": "Pressure tactic designed to make you skip verification"},
    {"phrase": "your account expires",           "weight": 2, "reason": "Fake account expiry threat used to create panic"},
    {"phrase": "within 24 hours",                "weight": 2, "reason": "Artificial deadline to prevent you from thinking carefully"},
    {"phrase": "action required",                "weight": 1, "reason": "Vague action demands are common in phishing messages"},

    # Prize / Lottery
    {"phrase": "you have won",                   "weight": 4, "reason": "Classic lottery/prize scam opener — you cannot win a contest you never entered"},
    {"phrase": "you've won",                     "weight": 4, "reason": "Classic lottery/prize scam opener — you cannot win a contest you never entered"},
    {"phrase": "you won",                        "weight": 3, "reason": "Unexpected win claims are a top scam tactic"},
    {"phrase": "you've been selected",           "weight": 4, "reason": "Fake selection notices are a common scam tactic"},
    {"phrase": "you have been selected",         "weight": 4, "reason": "Fake selection notices are a common scam tactic"},
    {"phrase": "claim your prize",               "weight": 4, "reason": "Lottery and prize scam language — real prizes do not require claiming fees"},
    {"phrase": "claim your reward",              "weight": 3, "reason": "Fake reward claim language used in prize scams"},
    {"phrase": "claim your",                     "weight": 2, "reason": "Claiming something unexpected is a common scam opener"},
    {"phrase": "your prize",                     "weight": 2, "reason": "Unexpected prize language is used in lottery scams"},
    {"phrase": "free gift",                      "weight": 2, "reason": "'Free' gifts in unsolicited messages often lead to hidden charges"},
    {"phrase": "million dollars",                "weight": 4, "reason": "Unrealistic prize claims are a clear scam sign"},
    {"phrase": "inheritance",                    "weight": 3, "reason": "Unexpected inheritance emails are a well-known advance-fee scam"},
    {"phrase": "unclaimed funds",                "weight": 3, "reason": "Fake fund recovery scam language"},
    {"phrase": "lottery winner",                 "weight": 4, "reason": "You cannot win a lottery you never entered"},
    {"phrase": "prize money",                    "weight": 3, "reason": "Unexpected prize money offers are almost always scams"},
    {"phrase": "congratulations you",            "weight": 2, "reason": "Prize/lottery scams commonly open with 'congratulations'"},

    # Payment / Financial demands
    {"phrase": "wire transfer",                  "weight": 3, "reason": "Scammers frequently demand wire transfers because they are nearly impossible to reverse"},
    {"phrase": "gift card",                      "weight": 4, "reason": "No legitimate government agency, bank, or business ever asks for gift card payments"},
    {"phrase": "bitcoin",                        "weight": 3, "reason": "Scammers use cryptocurrency because transactions are anonymous and irreversible"},
    {"phrase": "cryptocurrency",                 "weight": 2, "reason": "Requests for untraceable crypto payments are a strong scam signal"},
    {"phrase": "western union",                  "weight": 3, "reason": "Untraceable money wire service — a major scam payment red flag"},
    {"phrase": "money order",                    "weight": 2, "reason": "Untraceable payment method preferred by scammers"},
    {"phrase": "send money",                     "weight": 2, "reason": "Unexpected requests to send money to a stranger are a strong scam sign"},
    {"phrase": "send me money",                  "weight": 3, "reason": "Direct demand for money is a top scam signal"},
    {"phrase": "give me money",                  "weight": 3, "reason": "Direct money demand is a strong scam signal"},
    {"phrase": "pay me",                         "weight": 2, "reason": "Unexpected payment demands from strangers are suspicious"},
    {"phrase": "cash app",                       "weight": 2, "reason": "Scammers use Cash App to collect untraceable funds"},
    {"phrase": "cashapp",                        "weight": 2, "reason": "Scammers use Cash App to collect untraceable funds"},
    {"phrase": "venmo",                          "weight": 2, "reason": "Unexpected Venmo requests from strangers are a common scam tactic"},
    {"phrase": "zelle",                          "weight": 2, "reason": "Zelle scams are the fastest-growing form of payment fraud"},
    {"phrase": "routing number",                 "weight": 4, "reason": "Never share your bank routing number with someone who contacted you first"},
    {"phrase": "bank account number",            "weight": 4, "reason": "Requests for your account number from unsolicited contacts are a major red flag"},
    {"phrase": "pay a fee",                      "weight": 2, "reason": "Advance-fee scams charge upfront costs for services that do not exist"},
    {"phrase": "advance fee",                    "weight": 4, "reason": "Advance-fee fraud is one of the oldest and most common scam types"},
    {"phrase": "processing fee",                 "weight": 3, "reason": "Fake fees required to 'release' winnings or packages are a classic scam"},
    {"phrase": "transfer fee",                   "weight": 3, "reason": "Fake transfer fees to 'send you money' are a well-known scam tactic"},
    {"phrase": "registration fee",               "weight": 3, "reason": "Legitimate employers never charge a fee to start a job — this is always a scam"},
    {"phrase": "make a payment",                 "weight": 1, "reason": "Unsolicited payment requests should always be verified independently"},

    # Impersonation
    {"phrase": "this is the irs",                "weight": 4, "reason": "The IRS never contacts you first by phone or text — this is always a scam"},
    {"phrase": "irs",                            "weight": 1, "reason": "IRS impersonation is one of the top phone scam types reported to the FTC"},
    {"phrase": "social security number",         "weight": 4, "reason": "Never give your SSN to someone who contacted you — this is a major identity theft risk"},
    {"phrase": "ssn",                            "weight": 4, "reason": "Requests for your SSN from unsolicited contacts are a major red flag"},
    {"phrase": "social security",                "weight": 1, "reason": "Social Security Administration impersonation scams frequently target seniors"},
    {"phrase": "medicare",                       "weight": 2, "reason": "Medicare scams target seniors to steal personal information and benefits"},
    {"phrase": "amazon account team",            "weight": 3, "reason": "Amazon impersonation scam — always verify directly on amazon.com, never reply to the message"},
    {"phrase": "amazon account",                 "weight": 2, "reason": "Amazon account scams are very common — verify any claims on amazon.com directly"},
    {"phrase": "apple support",                  "weight": 2, "reason": "Tech support impersonation is a widespread scam — Apple never calls you unsolicited"},
    {"phrase": "microsoft support",              "weight": 2, "reason": "Microsoft tech support scams are extremely common — Microsoft never calls you unsolicited"},
    {"phrase": "microsoft",                      "weight": 1, "reason": "Microsoft is frequently impersonated in tech support scams"},
    {"phrase": "your account has been suspended","weight": 3, "reason": "Fake account suspension threats are used to steal your login credentials"},
    {"phrase": "account suspended",              "weight": 3, "reason": "Fake suspension notices are a phishing tactic to steal your credentials"},
    {"phrase": "account suspension",             "weight": 2, "reason": "Threats of account suspension are used to panic you into clicking phishing links"},
    {"phrase": "verify your account",            "weight": 3, "reason": "Phishing tactic designed to steal your username and password"},
    {"phrase": "confirm your identity",          "weight": 3, "reason": "Unsolicited identity confirmation requests are a common phishing technique"},
    {"phrase": "unusual sign",                   "weight": 2, "reason": "Fake 'unusual activity' alerts are used to create panic and phish for credentials"},
    {"phrase": "unusual activity",               "weight": 2, "reason": "Fake security alerts are commonly used in bank phishing scams"},
    {"phrase": "suspicious activity",            "weight": 2, "reason": "Fake suspicious activity notices are a common phishing trigger"},
    {"phrase": "warrant will be issued",         "weight": 4, "reason": "Fake arrest warrant threats are used to panic victims into paying immediately"},
    {"phrase": "arrest warrant",                 "weight": 4, "reason": "Government agencies never threaten arrest by phone or text — this is always a scam"},

    # Personal info harvesting
    {"phrase": "password",                       "weight": 2, "reason": "Legitimate companies never ask for your password — this is always a phishing attempt"},
    {"phrase": "verification code",              "weight": 3, "reason": "Scammers ask for your verification codes to take over your accounts"},
    {"phrase": "one-time code",                  "weight": 3, "reason": "Never share a one-time code with anyone who contacts you first"},
    {"phrase": "otp",                            "weight": 3, "reason": "Requests for your OTP (one-time password) are a major account takeover red flag"},
    {"phrase": "click here",                     "weight": 1, "reason": "Vague link instructions without context are common in phishing messages"},
    {"phrase": "click this link",                "weight": 2, "reason": "Directing you to click an unknown link is a phishing tactic"},
    {"phrase": "click the link",                 "weight": 2, "reason": "Directing you to click an unknown link is a phishing tactic"},
    {"phrase": "tap this link",                  "weight": 2, "reason": "Directing you to tap an unknown link is a phishing tactic"},
    {"phrase": "verify your information",        "weight": 2, "reason": "Phishing messages often request you to 'verify' personal information"},
    {"phrase": "update your billing",            "weight": 2, "reason": "Fake billing update requests are a common phishing tactic"},
    {"phrase": "confirm your details",           "weight": 2, "reason": "Phishing attempt to harvest your personal data"},

    # Romance / Trust
    {"phrase": "i love you",                     "weight": 1, "reason": "Romance scammers often profess love very quickly to build false trust"},
    {"phrase": "i need your help",               "weight": 1, "reason": "Emotional manipulation is a key romance scam tactic"},
    {"phrase": "stuck abroad",                   "weight": 3, "reason": "Classic travel emergency scam designed to extract money quickly"},
    {"phrase": "military romance",               "weight": 2, "reason": "Military romance scams are increasingly common on social media"},
    {"phrase": "deployed overseas",              "weight": 2, "reason": "Military deployment stories are frequently used in romance scams"},

    # Tech / Malware
    {"phrase": "your computer is infected",      "weight": 4, "reason": "Fake virus alert — a classic tech support scam designed to install malware or steal money"},
    {"phrase": "virus detected",                 "weight": 4, "reason": "Fake virus alerts are used to push victims into calling fake 'support' lines"},
    {"phrase": "call this number",               "weight": 2, "reason": "Scammers direct victims to call fake support lines to steal money or data"},
    {"phrase": "call us immediately",            "weight": 2, "reason": "High-pressure demand to call a fake support line is a scam tactic"},
    {"phrase": "remote access",                  "weight": 4, "reason": "Giving someone remote access to your computer lets scammers steal your data and money"},
    {"phrase": "download this",                  "weight": 2, "reason": "Unexpected download requests can install malware on your device"},

    # Delivery/package scams
    {"phrase": "your package",                   "weight": 1, "reason": "Fake package delivery notifications are used to phish for personal info or payment"},
    {"phrase": "delivery fee",                   "weight": 2, "reason": "Fake delivery fee demands are a common package scam — verify directly with the carrier"},
    {"phrase": "redelivery fee",                 "weight": 3, "reason": "No major carrier charges a redelivery fee via text link — this is almost always a scam"},
    {"phrase": "reschedule your delivery",       "weight": 1, "reason": "Fake delivery reschedule messages are used to trick you into clicking phishing links"},
    {"phrase": "usps",                           "weight": 1, "reason": "USPS is frequently impersonated in package delivery scams"},
    {"phrase": "fedex",                          "weight": 1, "reason": "FedEx is frequently impersonated in package delivery scams"},
    {"phrase": "ups",                            "weight": 1, "reason": "UPS is frequently impersonated in package delivery scams"},

    # Employment scams
    {"phrase": "work from home",                 "weight": 2, "reason": "Unsolicited work-from-home offers with fees are almost always employment scams"},
    {"phrase": "work-from-home",                 "weight": 2, "reason": "Unsolicited work-from-home offers with fees are almost always employment scams"},
    {"phrase": "earn per day",                   "weight": 2, "reason": "Guaranteed daily earnings claims in unsolicited offers are a red flag for job scams"},
    {"phrase": "earn per week",                  "weight": 2, "reason": "Guaranteed weekly earnings claims in unsolicited offers are a red flag for job scams"},
    {"phrase": "job opportunity",                "weight": 1, "reason": "Unsolicited job opportunities, especially with upfront fees, are commonly scams"},
    {"phrase": "get started today",              "weight": 1, "reason": "Pressure to start immediately is common in employment scams"},
]


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 2 — Regex patterns
# ──────────────────────────────────────────────────────────────────────────────
REGEX_PATTERNS = [
    # "give me 100", "give me $50", "give me 100 dollars"
    {
        "pattern": re.compile(
            r"\bgive\s+(?:me\s+)?(?:\$[\d,]+(?:\.\d{1,2})?|[\d,]+\$?(?:\s*dollars?)?)\b",
            re.IGNORECASE,
        ),
        "label": "give me [amount]",
        "weight": 3,
        "reason": "Demanding a specific amount of money from you is a strong scam signal",
    },
    # "send me $100", "send me 50 dollars"
    {
        "pattern": re.compile(
            r"\bsend\s+(?:me\s+)?(?:\$[\d,]+(?:\.\d{1,2})?|[\d,]+\$?(?:\s*dollars?)?)\b",
            re.IGNORECASE,
        ),
        "label": "send me [amount]",
        "weight": 3,
        "reason": "Requesting a specific money transfer from you is a scam warning sign",
    },
    # "pay me $200", "pay $99 to unlock", "pay a $75 fee"
    {
        "pattern": re.compile(
            r"\bpay\s+(?:(?:me|a|the|an)\s+)?(?:\$[\d,]+(?:\.\d{1,2})?|[\d,]+\$?(?:\s*dollars?)?)\b",
            re.IGNORECASE,
        ),
        "label": "pay [amount]",
        "weight": 3,
        "reason": "Demanding payment of a specific amount in an unsolicited message is suspicious",
    },
    # "transfer $500", "wire 200 dollars"
    {
        "pattern": re.compile(
            r"\b(?:transfer|wire)\s+(?:\$[\d,]+(?:\.\d{1,2})?|[\d,]+\$?(?:\s*dollars?)?)\b",
            re.IGNORECASE,
        ),
        "label": "transfer/wire [amount]",
        "weight": 3,
        "reason": "Requests to wire or transfer a specific amount are a classic advance-fee scam tactic",
    },
    # Unsolicited phone numbers
    {
        "pattern": re.compile(
            r"\b(?:call|contact|reach)\s+(?:us\s+)?(?:at\s+)?(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
            re.IGNORECASE,
        ),
        "label": "call [unverified phone number]",
        "weight": 2,
        "reason": "Directing you to call an unverified phone number in an unsolicited message is a scam tactic",
    },
    # Suspicious unknown URLs
    {
        "pattern": re.compile(
            r"\b(?!(?:[\w-]+\.)?(?:google|youtube|facebook|instagram|amazon|apple|microsoft|gov|ftc|irs|usa|usps|fedex|ups|streamlit|python|github|chase|wellsfargo|bankofamerica|citibank)\.)"
            r"[\w-]{2,}\.(?:com|net|org|info|biz|xyz|top|click|link|live|online|site|web|shop|store|verify|secure|update|alert)[/\w.-]*\b",
            re.IGNORECASE,
        ),
        "label": "unknown/suspicious link",
        "weight": 3,
        "reason": "Links to unknown or unfamiliar websites are a major phishing red flag — do not click",
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 3 — Context combinations
# ──────────────────────────────────────────────────────────────────────────────
CONTEXT_RULES = [
    # ── NEW: Bank / financial phishing with suspicious link ──────────────────
    {
        "signals": [
            ["bank", "chase", "wells fargo", "bank of america", "citibank", "credit union",
             "your account", "account activity", "sign-in", "login", "account alert",
             "security alert", "unusual sign", "unusual activity", "suspicious activity"],
            ["verify", "confirm", "confirm your identity", "update", "validate",
             "click", "tap", "visit", "go to", "log in", "sign in"],
            ["link", "here", "below", "secure", "website", "portal", "immediately",
             "avoid", "suspension", "suspended", "locked"],
        ],
        "weight": 5,
        "label": "bank phishing — fake security alert",
        "reason": "Fake bank security alerts asking you to verify via a link are a very common phishing scam — always go directly to your bank's official website instead",
    },
    # ── NEW: Delivery carrier + suspicious link + fee ────────────────────────
    {
        "signals": [
            ["usps", "fedex", "ups", "dhl", "postal service", "package", "parcel",
             "delivery", "shipment", "courier"],
            ["fee", "charge", "cost", "payment", "pay", "redelivery", "customs", "hold",
             "required", "outstanding"],
            ["link", "click", "here", "below", "now", "immediately", "today",
             "pay at", "visit", "parcel-", "pkg-", "track-",
             "parcel-redelivery", "redelivery.com", ".com/pay", "secure-",
             "unknown/suspicious"],
        ],
        "weight": 5,
        "label": "fake carrier — delivery fee phishing",
        "reason": "Fake delivery texts asking you to pay a fee via a link impersonate USPS/FedEx/UPS — official carriers never request payment by text link",
    },
    # ── NEW: Employment / job scam with fee ──────────────────────────────────
    {
        "signals": [
            ["selected", "chosen", "hired", "job offer", "position", "opportunity",
             "work from home", "work-from-home", "remote job", "earn"],
            ["fee", "registration", "deposit", "payment", "pay", "cost", "charge",
             "get started", "to begin", "to activate", "to access"],
            ["zelle", "venmo", "cash app", "cashapp", "bitcoin", "crypto", "wire",
             "gift card", "money order", "western union", "reply", "respond"],
        ],
        "weight": 5,
        "label": "job scam — upfront fee required",
        "reason": "Legitimate employers never ask you to pay a fee before starting work — this is always an employment scam",
    },
    # Unsolicited loan / financial offer + money amount + contact pressure
    {
        "signals": [
            ["loan", "mortgage", "refinance", "credit", "finance", "pre-approved", "pre approved"],
            ["calling you", "call you", "contacted you", "reaching out", "this call", "this message"],
            ["dollars", "payment", "fee", "deposit", "transfer", "amount", "money"],
        ],
        "weight": 4,
        "label": "unsolicited loan/financial contact",
        "reason": "Unsolicited calls or messages about loans with payment demands are a classic phone scam tactic",
    },
    # Impersonation + action demand
    {
        "signals": [
            ["i am", "i'm", "this is", "calling from", "calling on behalf"],
            ["bank", "government", "federal", "police", "sheriff", "officer", "agent",
             "statefarm", "state farm", "geico", "allstate", "insurance"],
            ["verify", "confirm", "provide", "send", "pay", "need", "require", "must"],
        ],
        "weight": 4,
        "label": "impersonation + action demand",
        "reason": "Someone claiming to be from an official organization and demanding action is a major red flag",
    },
    # Any money + urgency + contact method
    {
        "signals": [
            ["dollars", "payment", "fee", "deposit", "transfer", "money", "funds"],
            ["urgent", "immediately", "right away", "asap", "now", "today", "quick", "hurry"],
            ["call", "text", "reply", "respond", "click", "send", "wire"],
        ],
        "weight": 3,
        "label": "urgent money + contact demand",
        "reason": "Combining a money request with urgency and a contact method is a classic scam pattern",
    },
    # Prize / reward + personal info request
    {
        "signals": [
            ["won", "winner", "prize", "reward", "selected", "chosen", "lucky"],
            ["verify", "confirm", "provide", "send", "share", "give", "need"],
            ["name", "address", "number", "details", "information", "account", "social security", "id"],
        ],
        "weight": 4,
        "label": "prize claim + personal info request",
        "reason": "Requests for personal information to 'claim a prize' are always a scam",
    },
    # Romantic manipulation + financial request
    {
        "signals": [
            ["love", "miss you", "darling", "sweetheart", "baby", "honey", "dear"],
            ["money", "dollars", "send", "transfer", "help me", "need funds", "emergency"],
        ],
        "weight": 4,
        "label": "romantic manipulation + money request",
        "reason": "Romance scammers combine emotional language with unexpected money requests to exploit trust",
    },
    # Tech support + remote/download demand
    {
        "signals": [
            ["virus", "infected", "hacked", "malware", "error", "problem", "issue", "warning"],
            ["call", "download", "install", "click", "remote", "access", "technician", "support"],
            ["computer", "device", "pc", "phone", "laptop", "mac", "windows"],
        ],
        "weight": 4,
        "label": "fake tech support",
        "reason": "Unsolicited warnings about your device combined with demands to call or install something is a tech support scam",
    },
    # Overpayment / refund scam
    {
        "signals": [
            ["refund", "overpaid", "overpayment", "owe you", "return", "reimburse"],
            ["send back", "return the", "wire", "transfer", "pay back", "give back"],
            ["dollars", "amount", "money", "funds", "payment"],
        ],
        "weight": 4,
        "label": "overpayment/refund scam",
        "reason": "Being told you are owed a refund and must send money back is a classic overpayment scam",
    },
    # Delivery fee scam (general — carrier name not required)
    {
        "signals": [
            ["package", "parcel", "delivery", "shipment", "order"],
            ["pay", "payment", "fee", "charge", "cost", "click", "tap", "confirm"],
            ["link", "here", "below", "now", "immediately", "today", "hold", "released"],
        ],
        "weight": 3,
        "label": "suspicious delivery payment request",
        "reason": "Texts asking you to pay a fee via a link to release or redeliver a package are almost always phishing scams — check your carrier's official website instead",
    },
    # Gift card payment demand
    {
        "signals": [
            ["gift card", "gift cards", "itunes", "google play", "amazon card", "steam card"],
            ["pay", "purchase", "buy", "send", "use", "provide", "give"],
        ],
        "weight": 5,
        "label": "gift card payment demand",
        "reason": "No legitimate business, government agency, or utility company ever asks for payment in gift cards — this is always a scam",
    },
    # Upfront fee to claim prize or loan
    {
        "signals": [
            ["fee", "deposit", "processing", "tax", "advance", "upfront", "insurance", "customs"],
            ["release", "claim", "receive", "collect", "get", "unlock", "access"],
            ["prize", "winnings", "reward", "funds", "loan", "money", "inheritance", "package"],
        ],
        "weight": 4,
        "label": "upfront fee to claim prize or funds",
        "reason": "Any request for an upfront fee to release prize money, a loan, or funds is an advance-fee scam",
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# LEGITIMATE CONTEXT INDICATORS
# ──────────────────────────────────────────────────────────────────────────────
LEGITIMATE_SIGNALS = [
    re.compile(
        r"\b(?:school|class|homework|assignment|teacher|lunch|cafeteria|field trip|"
        r"permission slip|grade|student|tuition|fee is|cost is|costs\s+\$|"
        r"due\s+(?:date|by)|reminder)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:receipt|invoice|order\s+(?:number|#|confirmation)|tracking\s+number|"
        r"shipped|your\s+order|subscription renewal|monthly\s+(?:fee|charge|bill)|"
        r"statement|balance\s+due|payment\s+due)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:from\s+your\s+(?:bank|school|doctor|provider|carrier)|sent\s+by|"
        r"official\s+notice|do\s+not\s+reply|automated\s+message|no.?reply)\b",
        re.IGNORECASE,
    ),
]

NEUTRALISABLE_LABELS = {"dollar amount mentioned"}


def _has_legitimate_context(lower_text: str) -> bool:
    return any(pat.search(lower_text) for pat in LEGITIMATE_SIGNALS)


def _check_context_rules(lower_text: str) -> list[dict]:
    fired = []
    for rule in CONTEXT_RULES:
        all_groups_match = all(
            any(signal in lower_text for signal in group)
            for group in rule["signals"]
        )
        if all_groups_match:
            fired.append(rule)
    return fired


def analyze_message(text: str) -> dict:
    """
    Analyze a message for scam indicators using three layers:
      1. Plain-string keyword matching
      2. Regex pattern matching (money demands, phone numbers, suspicious links)
      3. Context-combination rules

    Returns dict with: score, verdict, color, reasons, matched_phrases, error
    """
    if not text or not text.strip():
        return {
            "score": 0,
            "verdict": "No message entered",
            "color": "warning",
            "reasons": [],
            "matched_phrases": [],
            "error": "empty",
        }

    lower_text = text.lower()
    legitimate = _has_legitimate_context(lower_text)
    total_weight = 0
    reasons = []
    matched_phrases = []
    credited_ranges = []

    # ── Layer 1: plain-string matching ───────────────────────────────────────
    sorted_patterns = sorted(SCAM_PATTERNS, key=lambda p: len(p["phrase"]), reverse=True)
    for pattern in sorted_patterns:
        phrase = pattern["phrase"]
        start = lower_text.find(phrase)
        if start == -1:
            continue
        end = start + len(phrase)
        if any(s <= start < e or s < end <= e for s, e in credited_ranges):
            continue
        if legitimate and pattern["weight"] <= 1:
            continue
        credited_ranges.append((start, end))
        total_weight += pattern["weight"]
        reasons.append(f"🚩 **'{phrase}'** — {pattern['reason']}")
        matched_phrases.append(phrase)

    # ── Layer 2: regex matching ───────────────────────────────────────────────
    for rp in REGEX_PATTERNS:
        match = rp["pattern"].search(text)
        if not match:
            continue
        start, end = match.start(), match.end()
        if any(s <= start < e or s < end <= e for s, e in credited_ranges):
            continue
        if legitimate and rp["label"] in NEUTRALISABLE_LABELS:
            continue
        credited_ranges.append((start, end))
        total_weight += rp["weight"]
        reasons.append(f"🚩 **'{rp['label']}'** — {rp['reason']}")
        matched_phrases.append(rp["label"])

    # ── Layer 3: context-combination rules ───────────────────────────────────
    # Augment lower_text with matched layer-2 labels so context rules can
    # "see" that a suspicious link was already detected by the regex layer.
    augmented_text = lower_text
    for mp in matched_phrases:
        augmented_text += " " + mp.lower()

    for rule in _check_context_rules(augmented_text):
        # Avoid double-counting if an identical label was already added by a prior rule
        if rule["label"] in matched_phrases:
            continue
        total_weight += rule["weight"]
        reasons.append(f"🚩 **'{rule['label']}'** — {rule['reason']}")
        matched_phrases.append(rule["label"])

    # ── Score ─────────────────────────────────────────────────────────────────
    # MAX_WEIGHT=20 calibration:
    #   1 mild (weight 1)            → score  5  → Safe
    #   1 moderate (weight 2-3)      → score 10-15 → Slightly Suspicious
    #   1 strong (weight 4-5)        → score 20-25 → Slightly / Suspicious
    #   2 strong signals             → score 40-50 → Suspicious
    #   1 strong + 1 context rule    → score 60+  → Likely Scam
    MAX_WEIGHT = 20
    score = min(int((total_weight / MAX_WEIGHT) * 100), 100)

    # ── Verdict ───────────────────────────────────────────────────────────────
    if score < 15:
        verdict = "Looks Safe"
        color   = "success"
    elif score < 35:
        verdict = "Slightly Suspicious"
        color   = "info"
    elif score < 60:
        verdict = "Suspicious — Be Careful"
        color   = "warning"
    else:
        verdict = "Likely a Scam — Do NOT respond"
        color   = "error"

    return {
        "score": score,
        "verdict": verdict,
        "color": color,
        "reasons": reasons,
        "matched_phrases": matched_phrases,
        "error": None,
    }
