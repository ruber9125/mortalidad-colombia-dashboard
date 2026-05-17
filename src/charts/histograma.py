import plotly.express as px

from src.helpers import apply_common_layout


def build_histograma_figure(df):
    histograma_edades = df.dropna(
        subset=["GRUPO_EDAD1_NUM"]
    ).copy()

    histograma_edades["GRUPO_EDAD1"] = (
        histograma_edades["GRUPO_EDAD1_NUM"].astype(int).astype(str)
    )

    age_order = sorted(histograma_edades["GRUPO_EDAD1_NUM"].astype(int).unique())
    age_order = [str(value) for value in age_order]

    figure = px.histogram(
        histograma_edades,
        x="GRUPO_EDAD1",
        category_orders={"GRUPO_EDAD1": age_order},
        title="Distribución de muertes por código GRUPO_EDAD1",
        labels={
            "GRUPO_EDAD1": "Código de grupo de edad",
            "count": "Muertes",
        },
    )
    apply_common_layout(figure)
    return figure
