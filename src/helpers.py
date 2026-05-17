import unicodedata

import pandas as pd


def normalize_text(value):
    if pd.isna(value):
        return ""

    return (
        unicodedata.normalize("NFKD", str(value))
        .encode("ascii", "ignore")
        .decode("ascii")
        .strip()
        .lower()
    )


def detect_cause_columns(catalog):
    normalized_columns = {
        column: normalize_text(column)
        for column in catalog.columns
    }

    code_column = next(
        (
            column
            for column, normalized in normalized_columns.items()
            if "codigo" in normalized
        ),
        None,
    )

    description_column = next(
        (
            column
            for column, normalized in normalized_columns.items()
            if "descripcion" in normalized or "causa" in normalized
        ),
        None,
    )

    if code_column is None and len(catalog.columns) >= 1:
        code_column = catalog.columns[0]

    if description_column is None:
        remaining = [
            column
            for column in catalog.columns
            if column != code_column
        ]

        if remaining:
            description_column = remaining[0]

    return code_column, description_column


def add_city_label(frame):
    labeled = frame.copy()
    labeled["CIUDAD"] = labeled["MUNICIPIO"] + " - " + labeled["DEPARTAMENTO"]
    return labeled


def apply_common_layout(figure):
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=20, t=70, b=40),
        title_x=0.02,
    )
    return figure
