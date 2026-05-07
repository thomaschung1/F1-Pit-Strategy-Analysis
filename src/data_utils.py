# =========================================================
# CONSTRUCTOR NAME NORMALIZATION
# =========================================================

def clean_constructor_names(df):
    constructor_mapping = {
        # Minor formatting consistency
        "Alpine F1 Team": "Alpine",
        "Haas F1 Team": "Haas",
        "Kick Sauber": "Sauber",
        "Lotus F1" : "Lotus",
        "Manor Marussia": "Marussia",
        "RB F1 Team": "Racing Bulls",
        "Red Bull": "Red Bull Racing"
    }

    df = df.copy()
    df["constructor_clean"] = (
        df["constructor_name"]
        .replace(constructor_mapping)
    )
    
    return df