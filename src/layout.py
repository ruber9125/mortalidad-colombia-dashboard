from dash import dash_table, dcc, html

from src.config import (
    APP_AUTHOR,
    APP_AUTHOR_LABEL,
    APP_HERO_SUBTITLE,
    APP_HERO_TITLE,
    APP_INSTITUTION,
    GRAPH_CONFIG,
    TABLE_TITLE,
)


def create_graph_card(figure):
    return html.Div(
        [
            dcc.Graph(
                figure=figure,
                config=GRAPH_CONFIG,
                className="chart-graph",
            ),
        ],
        className="dashboard-card",
    )


def create_metric_card(metric):
    return html.Div(
        [
            html.P(metric["label"], className="metric-label"),
            html.P(metric["value"], className="metric-value"),
            html.P(metric.get("note", ""), className="metric-note", hidden=not metric.get("note")),
        ],
        className=f"metric-card accent-{metric['accent']}",
    )


def create_causes_table_card(tabla_causas, causes_warning):
    return html.Div(
        [
            html.Div(
                [
                    html.H2(TABLE_TITLE, className="section-title"),
                    html.P(
                        "Cruce entre COD_MUERTE del dataset principal y el catalogo CIE-10 cargado.",
                        className="section-caption",
                    ),
                ],
                className="section-heading",
            ),
            html.Div(
                causes_warning,
                className="warning-banner",
                hidden=not bool(causes_warning),
            ),
            dash_table.DataTable(
                data=tabla_causas.to_dict("records"),
                columns=[
                    {
                        "name": column,
                        "id": column,
                    }
                    for column in tabla_causas.columns
                ],
                style_table={
                    "overflowX": "auto",
                    "border": "1px solid rgba(148, 163, 184, 0.14)",
                    "borderRadius": "14px",
                },
                style_cell={
                    "textAlign": "left",
                    "padding": "14px",
                    "whiteSpace": "normal",
                    "height": "auto",
                    "fontFamily": "Segoe UI, Tahoma, sans-serif",
                    "backgroundColor": "#111827",
                    "color": "#e5eefb",
                    "border": "1px solid rgba(148, 163, 184, 0.12)",
                },
                style_header={
                    "fontWeight": "bold",
                    "backgroundColor": "#182132",
                    "color": "#f8fafc",
                    "border": "1px solid rgba(148, 163, 184, 0.14)",
                    "textTransform": "uppercase",
                    "letterSpacing": "0.04em",
                },
                style_data={
                    "backgroundColor": "#111827",
                },
            ),
        ],
        className="dashboard-card",
    )


def create_layout(
    summary_metrics,
    fig_mapa,
    fig_lineas,
    fig_barras,
    fig_pie,
    fig_stack,
    fig_hist,
    tabla_causas,
    causes_warning,
):
    return html.Div(
        [
            html.Header(
                [
                    html.Div(className="hero-glow hero-glow-left"),
                    html.Div(className="hero-glow hero-glow-right"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("Dashboard analitico", className="hero-kicker"),
                                    html.P(APP_INSTITUTION, className="hero-institution"),
                                ],
                                className="hero-top-copy",
                            ),
                        ],
                        className="hero-topbar",
                    ),
                    html.H1(APP_HERO_TITLE, className="hero-title"),
                    html.P(APP_HERO_SUBTITLE, className="hero-subtitle"),
                    html.P(
                        [
                            html.Span(f"{APP_AUTHOR_LABEL} "),
                            html.Strong(APP_AUTHOR),
                        ],
                        className="hero-author",
                    ),
                ],
                className="hero-section",
            ),
            html.Section(
                [create_metric_card(metric) for metric in summary_metrics],
                className="metrics-grid",
            ),
            html.Section(
                [
                    html.Div(create_graph_card(fig_mapa), className="span-12"),
                    html.Div(create_graph_card(fig_lineas), className="span-6"),
                    html.Div(create_graph_card(fig_stack), className="span-6"),
                    html.Div(create_graph_card(fig_barras), className="span-6"),
                    html.Div(create_graph_card(fig_pie), className="span-6"),
                    html.Div(
                        create_causes_table_card(tabla_causas, causes_warning),
                        className="span-12",
                    ),
                    html.Div(create_graph_card(fig_hist), className="span-12"),
                ],
                className="charts-grid",
            ),
        ],
        className="page-container",
    )
