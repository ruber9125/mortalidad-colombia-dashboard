import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
GEOJSON_DIR = BASE_DIR / "geojson"
ASSETS_DIR = BASE_DIR / "assets"

MAIN_DATASET_PATH = DATA_DIR / "mortalidad_2019.csv"
DIVIPOLA_PATH = DATA_DIR / "Divipola_CE_.xlsx"
CAUSE_CATALOG_ENV_PATH = os.getenv("CAUSE_CATALOG_PATH", "").strip()
CAUSE_CATALOG_PATH = DATA_DIR / "Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
CAUSE_CATALOG_GLOBS = [
    "*CodigosDeMuerte*.xlsx",
    "*CodigosDeMuerte*.xls",
    "*CodigosDeMuerte*.csv",
    "*codigosdemuerte*.xlsx",
    "*codigosdemuerte*.xls",
    "*codigosdemuerte*.csv",
]
GEOJSON_CANDIDATES = [
    GEOJSON_DIR / "colombia_real.geojson",
    GEOJSON_DIR / "colombia.geojson",
]

MONTH_NAMES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

EXPECTED_MAIN_COLUMNS = [
    "COD_DANE",
    "COD_DEPARTAMENTO",
    "COD_MUNICIPIO",
    "AREA_DEFUNCION",
    "SITIO_DEFUNCION",
    "AÑO",
    "MES",
    "HORA",
    "MINUTOS",
    "SEXO",
    "ESTADO_CIVIL",
    "GRUPO_EDAD1",
    "NIVEL_EDUCATIVO",
    "MANERA_MUERTE",
    "COD_MUERTE",
    "IDPROFESIONAL",
]

EXPECTED_DIVIPOLA_COLUMNS = [
    "COD_DANE",
    "COD_DEPARTAMENTO",
    "DEPARTAMENTO",
    "COD_MUNICIPIO",
    "MUNICIPIO",
    "FECHA1erFIS",
]

FEATURE_ID_COLUMN = "DPTO"

APP_TITLE = "Análisis de Mortalidad en Colombia - 2019"
APP_SUBTITLE = (
    "Dashboard exploratorio con validación de merge, limpieza de códigos y "
    "visualización por territorio, tiempo, causa, sexo y edad."
)
APP_HERO_TITLE = "Mortalidad en Colombia — 2019"
APP_HERO_SUBTITLE = (
    "Dashboard analítico e interactivo construido con Dash y Plotly a partir "
    "de microdatos de mortalidad del DANE."
)
APP_INSTITUTION = "Universidad de La Salle"
APP_AUTHOR = "Rubert Eduardo Quintero Orozco"
APP_AUTHOR_LABEL = "Proyecto desarrollado por"
TABLE_TITLE = "Top 10 causas de muerte"

GRAPH_CONFIG = {"displayModeBar": False}
