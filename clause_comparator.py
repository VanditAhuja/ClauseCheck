STANDARD_CLAUSES = [

    "Coverage",

    "Premium",

    "Claim",

    "Nominee",

    "Cancellation",

    "Exclusions",

    "Policy Period",

    "Renewal"

]


def compare_clauses(text):

    found = []

    missing = []

    lower_text = text.lower()

    for clause in STANDARD_CLAUSES:

        if clause.lower() in lower_text:

            found.append(clause)

        else:

            missing.append(clause)

    return {

        "found": found,

        "missing": missing

    }