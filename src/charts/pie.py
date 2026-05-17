import plotly.express as px

from src.helpers import add_city_label, apply_common_layout


def build_pie_figure(df):
    menor_mortalidad = (
        df.groupby(
            [
                "DEPARTAMENTO",
                "MUNICIPIO",
            ],
            dropna=False,
        )
        .size()
        .reset_index(name="TOTAL")
        .sort_values(
            by=["TOTAL", "DEPARTAMENTO", "MUNICIPIO"],
            ascending=[True, True, True],
        )
        .head(10)
    )

    menor_mortalidad = add_city_label(menor_mortalidad)

    figure = px.pie(
        menor_mortalidad,
        names="CIUDAD",
        values="TOTAL",
        title="10 municipios con menor número de muertes registradas",
    )
    apply_common_layout(figure)
    return figure
