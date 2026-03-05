from rapidfuzz import fuzz

def is_duplicate(existing, incoming):

    # Strict email match
    if existing.email and incoming.email:
        if existing.email.strip().lower() == incoming.email.strip().lower():
            return True

    # Strict phone match
    if existing.phone and incoming.phone:
        if existing.phone.strip() == incoming.phone.strip():
            return True

    return False