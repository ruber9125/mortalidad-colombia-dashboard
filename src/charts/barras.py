import plotly.express as px

from src.helpers import add_city_label, apply_common_layout


def build_barras_figure(df):
    homicidios = df[
        df["COD_MUERTE"].str.startswith("X95", na=False)
    ].copy()

    print(
        "Registros X95 exactos:",
        int((df["COD_MUERTE"] == "X95").sum()),
    )
    print(
        "Registros familia X95*:",
        len(homicidios),
    )

    top5 = (
        homicidios.groupby(
            [
                "DEPARTAMENTO",
                "MUNICIPIO",
            ],
            dropna=False,
        )
        .size()
        .reset_index(name="TOTAL")
        .sort_values(
            by="TOTAL",
            ascending=False,
        )
        .head(5)
    )

    top5 = add_city_label(top5)

    figure = px.bar(
        top5,
        x="CIUDAD",
        y="TOTAL",
        text="TOTAL",
        color="TOTAL",
        color_continuous_scale="Reds",
        title="Top 5 ciudades con más homicidios (familia X95*)",
        labels={
            "CIUDAD": "Ciudad",
            "TOTAL": "Homicidios",
        },
    )
    apply_common_layout(figure)
    return figure
