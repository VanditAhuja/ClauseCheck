HIGH_RISK = [

    "without notice",

    "non-refundable",

    "auto renew",

    "penalty",

    "late fee",

    "waive",

    "terminate immediately",

    "liability"

]


def detect_risk(text):

    risks = []

    lower = text.lower()

    for word in HIGH_RISK:

        if word in lower:

            risks.append(word)

    return risks