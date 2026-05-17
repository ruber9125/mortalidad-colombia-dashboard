from src.validators import validate_merge_row_count


def build_divipola_lookup(divipola):
    return divipola[
        [
            "COD_DANE",
            "DEPARTAMENTO",
            "MUNICIPIO",
        ]
    ].drop_duplicates(subset="COD_DANE")


def merge_with_divipola(df, divipola):
    divipola_lookup = build_divipola_lookup(divipola)

    rows_before_merge = len(df)
    print(f"len(df) antes del merge: {rows_before_merge}")

    merged = df.merge(
        divipola_lookup,
        on="COD_DANE",
        how="left",
        validate="many_to_one",
    )

    rows_after_merge = len(merged)
    print(f"len(df) después del merge: {rows_after_merge}")

    validate_merge_row_count(rows_before_merge, rows_after_merge)

    print(
        "Nulos tras merge:",
        {
            "DEPARTAMENTO": int(merged["DEPARTAMENTO"].isna().sum()),
            "MUNICIPIO": int(merged["MUNICIPIO"].isna().sum()),
        },
    )

    return merged
