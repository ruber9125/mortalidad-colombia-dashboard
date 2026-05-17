import os

from dash import Dash

from src.charts.barras import build_barras_figure
from src.charts.histograma import build_histograma_figure
from src.charts.lineas import build_lineas_figure
from src.charts.mapa import build_mapa_figure
from src.charts.pie import build_pie_figure
from src.charts.stack import build_stack_figure
from src.charts.tabla import build_tabla_causas
from src.cleaners import (
    clean_cause_catalog,
    clean_divipola_dataset,
    clean_main_dataset,
)
from src.config import EXPECTED_DIVIPOLA_COLUMNS, EXPECTED_MAIN_COLUMNS
from src.layout import create_layout
from src.loaders import (
    load_cause_catalog,
    load_divipola_dataset,
    load_main_dataset,
    load_valid_geojson,
)
from src.services.age_service import add_numeric_columns
from src.services.geo_service import (
    get_geojson_department_codes,
    get_geojson_properties,
)
from src.services.merge_service import merge_with_divipola
from src.services.summary_service import build_summary_metrics
from src.validators import validate_expected_columns


def load_dashboard_resources():
    df = load_main_dataset()
    divipola = load_divipola_dataset()
    codigos, codigos_path = load_cause_catalog()
    colombia_geojson, _geojson_path = load_valid_geojson()

    print("df.columns:")
    print(df.columns)
    print("divipola.columns:")
    print(divipola.columns)

    if codigos is not None:
        print("codigos.columns:")
        print(codigos.columns)
        print("Catalogo de causas usado:")
        print(codigos_path)

    geojson_properties = get_geojson_properties(colombia_geojson)
    print("Propiedades GeoJSON:")
    print(geojson_properties)

    validate_expected_columns(
        df,
        divipola,
        EXPECTED_MAIN_COLUMNS,
        EXPECTED_DIVIPOLA_COLUMNS,
    )

    df = clean_main_dataset(df)
    divipola = clean_divipola_dataset(divipola)
    codigos = clean_cause_catalog(codigos)

    df = merge_with_divipola(df, divipola)
    df = add_numeric_columns(df)

    geojson_department_codes = get_geojson_department_codes(colombia_geojson)

    return df, codigos, colombia_geojson, geojson_department_codes


df, codigos, colombia_geojson, geojson_department_codes = load_dashboard_resources()

summary_metrics = build_summary_metrics(df)
fig_mapa = build_mapa_figure(
    df,
    colombia_geojson,
    geojson_department_codes,
)
fig_lineas = build_lineas_figure(df)
fig_barras = build_barras_figure(df)
fig_pie = build_pie_figure(df)
fig_stack = build_stack_figure(df)
fig_hist = build_histograma_figure(df)
tabla_causas, causes_warning = build_tabla_causas(codigos, df)

app = Dash(__name__)
server = app.server

app.layout = create_layout(
    summary_metrics,
    fig_mapa,
    fig_lineas,
    fig_barras,
    fig_pie,
    fig_stack,
    fig_hist,
    tabla_causas,
    causes_warning,
)


if __name__ == "__main__":
    host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"

    app.run(
        debug=True,
        host=host,
        port=int(os.getenv("PORT", "8050")),
    )
