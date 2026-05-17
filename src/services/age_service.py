import pandas as pd


def add_numeric_columns(df):
    normalized = df.copy()
    normalized["MES_NUM"] = pd.to_numeric(
        normalized["MES"],
        errors="coerce",
    )
    normalized["GRUPO_EDAD1_NUM"] = pd.to_numeric(
        normalized["GRUPO_EDAD1"],
        errors="coerce",
    )
    return normalized
