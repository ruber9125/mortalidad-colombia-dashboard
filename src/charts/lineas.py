import plotly.express as px

from src.config import MONTH_NAMES
from src.helpers import apply_common_layout


def build_lineas_figure(df):
    muertes_mes = (
        df.dropna(subset=["MES_NUM"])
        .groupby("MES_NUM")
        .size()
        .reset_index(name="TOTAL")
        .sort_values("MES_NUM")
    )

    muertes_mes["MES_NUM"] = muertes_mes["MES_NUM"].astype(int)
    muertes_mes["MES"] = muertes_mes["MES_NUM"].map(MONTH_NAMES)

    figure = px.line(
        muertes_mes,
        x="MES",
        y="TOTAL",
        markers=True,
        category_orders={"MES": list(MONTH_NAMES.values())},
        title="Total de muertes por mes en Colombia - 2019",
        labels={
            "MES": "Mes",
            "TOTAL": "Muertes",
        },
    )
    apply_common_layout(figure)
    return figure
