from src.config import FEATURE_ID_COLUMN


def validate_expected_columns(
    df,
    divipola,
    expected_main_columns,
    expected_divipola_columns,
):
    missing_main_columns = sorted(set(expected_main_columns) - set(df.columns))
    missing_divipola_columns = sorted(
        set(expected_divipola_columns) - set(divipola.columns)
    )

    if missing_main_columns:
        raise ValueError(
            f"Faltan columnas en el dataset principal: {missing_main_columns}"
        )

    if missing_divipola_columns:
        raise ValueError(
            f"Faltan columnas en DIVIPOLA: {missing_divipola_columns}"
        )


def validate_geojson_feature_id(geojson_properties):
    if FEATURE_ID_COLUMN not in geojson_properties:
        raise ValueError(
            "El GeoJSON no contiene la propiedad 'DPTO' necesaria "
            "para cruzar departamentos."
        )


def validate_merge_row_count(rows_before_merge, rows_after_merge):
    if rows_before_merge != rows_after_merge:
        raise ValueError("El merge con DIVIPOLA multiplicó o eliminó filas.")
