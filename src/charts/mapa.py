import plotly.express as px

from src.config import FEATURE_ID_COLUMN
from src.helpers import apply_common_layout


def build_mapa_figure(df, geojson_data, geojson_department_codes):
    muertes_departamento = (
        df.groupby(
            [
                "COD_DEPARTAMENTO",
                "DEPARTAMENTO",
            ],
            dropna=False,
        )
        .size()
        .reset_index(name="TOTAL")
    )

    muertes_departamento["COD_DEPARTAMENTO"] = (
        muertes_departamento["COD_DEPARTAMENTO"].astype(str).str.zfill(2)
    )

    missing_geojson_codes = sorted(
        set(muertes_departamento["COD_DEPARTAMENTO"]) - geojson_department_codes
    )
    print("Departamentos fuera del GeoJSON:", missing_geojson_codes)
    print(f"featureidkey usado: properties.{FEATURE_ID_COLUMN}")

    figure = px.choropleth(
        muertes_departamento,
        geojson=geojson_data,
        locations="COD_DEPARTAMENTO",
        featureidkey=f"properties.{FEATURE_ID_COLUMN}",
        color="TOTAL",
        hover_name="DEPARTAMENTO",
        color_continuous_scale="Reds",
        title="Total de muertes por departamento en Colombia - 2019",
        labels={
            "TOTAL": "Muertes",
            "COD_DEPARTAMENTO": "Código DANE",
        },
    )
    figure.update_geos(
        fitbounds="locations",
        visible=False,
    )
    apply_common_layout(figure)
    return figure
