import plotly.express as px

from src.helpers import apply_common_layout


SEX_LABELS = {
    "1": "Hombres",
    "2": "Mujeres",
}

SEX_COLORS = {
    "Hombres": "#5aa2ff",
    "Mujeres": "#ffd21f",
    "Sin dato": "#94a3b8",
}

DEPARTMENT_LABELS = {
    "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA": "SAN ANDRÉS Y PROVIDENCIA",
}


def build_stack_figure(df):
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
        .sort_values("TOTAL", ascending=False)
    )

    department_order = muertes_departamento["DEPARTAMENTO"].tolist()
    department_order_labels = [
        DEPARTMENT_LABELS.get(department, department)
        for department in department_order
    ]

    sexo_departamento = (
        df.groupby(
            [
                "DEPARTAMENTO",
                "SEXO",
            ],
            dropna=False,
        )
        .size()
        .reset_index(name="TOTAL")
    )

    sexo_departamento["SEXO_LABEL"] = (
        sexo_departamento["SEXO"]
        .fillna("")
        .astype(str)
        .str.strip()
        .map(SEX_LABELS)
        .fillna("Sin dato")
    )
    sexo_departamento["DEPARTAMENTO_LABEL"] = (
        sexo_departamento["DEPARTAMENTO"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace(DEPARTMENT_LABELS)
    )

    sexo_order = [
        sex_label
        for sex_label in ["Hombres", "Mujeres", "Sin dato"]
        if sex_label in sexo_departamento["SEXO_LABEL"].unique()
    ]

    figure = px.bar(
        sexo_departamento,
        x="DEPARTAMENTO_LABEL",
        y="TOTAL",
        color="SEXO_LABEL",
        barmode="stack",
        category_orders={
            "DEPARTAMENTO_LABEL": department_order_labels,
            "SEXO_LABEL": sexo_order,
        },
        color_discrete_map=SEX_COLORS,
        title="Distribución de muertes por sexo en cada departamento",
        labels={
            "DEPARTAMENTO_LABEL": "Departamento",
            "TOTAL": "Muertes",
            "SEXO_LABEL": "Sexo",
        },
        hover_data={
            "DEPARTAMENTO": True,
            "DEPARTAMENTO_LABEL": False,
            "TOTAL": ":,",
            "SEXO_LABEL": True,
        },
    )
    apply_common_layout(figure)
    figure.update_layout(
        height=420,
        title=dict(
            font=dict(size=22),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
            font=dict(size=11),
        ),
        margin=dict(l=40, r=24, t=90, b=120),
    )
    figure.update_xaxes(
        tickangle=45,
        tickfont=dict(size=10),
        title_font=dict(size=14),
        automargin=True,
    )
    figure.update_yaxes(
        showgrid=True,
        gridcolor="#dbe2ea",
        zeroline=False,
        tickfont=dict(size=11),
        title_font=dict(size=14),
    )
    return figure
