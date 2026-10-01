# Part3_Narrative/masking.py

def alias_for(reseller_id: str) -> str:
    """
    Convert reseller_id like RS019 -> ALIAS-19
    """
    return f"ALIAS-{reseller_id[2:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """
    Return False if any raw reseller_name appears in text.
    """
    for name in reseller_names:
        if name in text:
            return False
    return True


if __name__ == "__main__":
    # Example narrative using aliases only
    narrative = (
        "Top reseller in West region is ALIAS-19, "
        "followed by ALIAS-22, ALIAS-12, ALIAS-06, ALIAS-05."
    )
    reseller_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    # Positive case: no raw names leak
    print(assert_no_raw_names_leak(narrative, reseller_names))  # True

    # Negative case: raw name present
    bad_narrative = "Mumbai Reseller 1 had highest spend."
    print(assert_no_raw_names_leak(bad_narrative, reseller_names))  # False

    # Alias function demo
    print(alias_for("RS019"))  # ALIAS-19
