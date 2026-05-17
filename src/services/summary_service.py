def _format_integer(value):
    return f"{int(value):,}"


def _format_percentage(value):
    return f"{value:.1f}%"


def build_summary_metrics(df):
    total_defunciones = len(df)
    homicidios_x95 = int(df["COD_MUERTE"].str.startswith("X95", na=False).sum())

    valid_sex = df["SEXO"].fillna("").astype(str).str.strip()
    known_sex = valid_sex.isin(["1", "2"])
    known_sex_total = int(known_sex.sum())
    male_count = int((valid_sex == "1").sum())
    female_count = int((valid_sex == "2").sum())
    male_percentage = (
        (male_count / known_sex_total * 100)
        if known_sex_total > 0
        else 0.0
    )
    female_percentage = (
        (female_count / known_sex_total * 100)
        if known_sex_total > 0
        else 0.0
    )

    return [
        {
            "label": "Total de defunciones",
            "value": _format_integer(total_defunciones),
            "accent": "teal",
        },
        {
            "label": "Hombres",
            "value": _format_integer(male_count),
            "note": _format_percentage(male_percentage),
            "accent": "blue",
        },
        {
            "label": "Mujeres",
            "value": _format_integer(female_count),
            "note": _format_percentage(female_percentage),
            "accent": "gold",
        },
        {
            "label": "Homicidios (familia X95*)",
            "value": _format_integer(homicidios_x95),
            "accent": "coral",
        },
    ]
