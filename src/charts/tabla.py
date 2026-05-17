import pandas as pd

from src.helpers import normalize_text


def _find_catalog_columns(catalog):
    normalized_columns = {
        column: normalize_text(column)
        for column in catalog.columns
    }

    code_4_column = next(
        (
            column
            for column, normalized in normalized_columns.items()
            if "codigo" in normalized and "cuatro" in normalized
        ),
        None,
    )
    description_4_column = next(
        (
            column
            for column, normalized in normalized_columns.items()
            if "descripcion" in normalized and "cuatro" in normalized
        ),
        None,
    )
    code_3_column = next(
        (
            column
            for column, normalized in normalized_columns.items()
            if "codigo" in normalized and "tres" in normalized
        ),
        None,
    )
    description_3_column = next(
        (
            column
            for column, normalized in normalized_columns.items()
            if "descripcion" in normalized and "tres" in normalized
        ),
        None,
    )

    return {
        "code_4": code_4_column,
        "description_4": description_4_column,
        "code_3": code_3_column,
        "description_3": description_3_column,
    }


def build_tabla_causas(catalog, df):
    causes_warning = None

    tabla_causas = (
        df.groupby("COD_MUERTE")
        .size()
        .reset_index(name="TOTAL")
        .sort_values(
            by="TOTAL",
            ascending=False,
        )
        .head(10)
    )

    if catalog is not None:
        catalog_columns = _find_catalog_columns(catalog)

        code_4_column = catalog_columns["code_4"]
        description_4_column = catalog_columns["description_4"]
        code_3_column = catalog_columns["code_3"]
        description_3_column = catalog_columns["description_3"]

        has_four_char_lookup = code_4_column and description_4_column
        has_three_char_lookup = code_3_column and description_3_column

        if has_four_char_lookup or has_three_char_lookup:
            enriched = tabla_causas.copy()

            if has_four_char_lookup:
                catalogo_causas_4 = (
                    catalog[
                        [
                            code_4_column,
                            description_4_column,
                        ]
                    ]
                    .rename(
                        columns={
                            code_4_column: "COD_MUERTE",
                            description_4_column: "DESCRIPCION_4",
                        }
                    )
                    .drop_duplicates(subset="COD_MUERTE")
                )

                enriched = enriched.merge(
                    catalogo_causas_4,
                    on="COD_MUERTE",
                    how="left",
                    validate="many_to_one",
                )
            else:
                enriched["DESCRIPCION_4"] = pd.NA

            if has_three_char_lookup:
                enriched["COD_MUERTE_3"] = enriched["COD_MUERTE"].astype(str).str[:3]
                catalogo_causas_3 = (
                    catalog[
                        [
                            code_3_column,
                            description_3_column,
                        ]
                    ]
                    .rename(
                        columns={
                            code_3_column: "COD_MUERTE_3",
                            description_3_column: "DESCRIPCION_3",
                        }
                    )
                    .drop_duplicates(subset="COD_MUERTE_3")
                )

                enriched = enriched.merge(
                    catalogo_causas_3,
                    on="COD_MUERTE_3",
                    how="left",
                    validate="many_to_one",
                )
            else:
                enriched["DESCRIPCION_3"] = pd.NA

            enriched["DESCRIPCION"] = (
                enriched["DESCRIPCION_4"]
                .replace("", pd.NA)
                .fillna(enriched["DESCRIPCION_3"].replace("", pd.NA))
                .fillna("Sin descripcion en el anexo")
            )

            tabla_causas = enriched[
                [
                    "COD_MUERTE",
                    "DESCRIPCION",
                    "TOTAL",
                ]
            ]
        else:
            tabla_causas["DESCRIPCION"] = ""
            causes_warning = (
                "No fue posible identificar automaticamente las columnas de "
                "codigo y descripcion en el catalogo de causas."
            )
    else:
        tabla_causas["DESCRIPCION"] = ""
        causes_warning = (
            "No se cargo el catalogo de causas. Los codigos si provienen del "
            "dataset principal, pero la descripcion humana no esta disponible."
        )

    tabla_causas = tabla_causas.rename(
        columns={
            "COD_MUERTE": "CODIGO",
        }
    )[
        [
            "CODIGO",
            "DESCRIPCION",
            "TOTAL",
        ]
    ]

    return tabla_causas, causes_warning
