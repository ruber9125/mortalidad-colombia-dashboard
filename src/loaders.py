import json
from pathlib import Path

import pandas as pd

from src.config import (
    CAUSE_CATALOG_ENV_PATH,
    CAUSE_CATALOG_GLOBS,
    CAUSE_CATALOG_PATH,
    DIVIPOLA_PATH,
    GEOJSON_CANDIDATES,
    MAIN_DATASET_PATH,
)


def load_main_dataset():
    return pd.read_csv(
        MAIN_DATASET_PATH,
        sep=";",
        dtype=str,
    )


def load_divipola_dataset():
    return pd.read_excel(
        DIVIPOLA_PATH,
        dtype=str,
    )


def _read_cause_catalog(path):
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(
            path,
            sep=";",
            dtype=str,
            encoding="utf-8-sig",
            skiprows=8,
        )

    return pd.read_excel(path, dtype=str)


def load_cause_catalog():
    if CAUSE_CATALOG_ENV_PATH:
        env_path = Path(CAUSE_CATALOG_ENV_PATH).expanduser()

        if env_path.exists():
            print(f"Catalogo de causas cargado desde CAUSE_CATALOG_PATH: {env_path}")
            return _read_cause_catalog(env_path), env_path

        print("CAUSE_CATALOG_PATH fue definido pero no existe:", env_path)

    exact_candidates = [
        CAUSE_CATALOG_PATH,
        CAUSE_CATALOG_PATH.with_suffix(".csv"),
    ]

    for path in exact_candidates:
        if path.exists():
            print(f"Catalogo de causas cargado desde ruta exacta: {path}")
            return _read_cause_catalog(path), path

    candidates = []

    for pattern in CAUSE_CATALOG_GLOBS:
        candidates.extend(CAUSE_CATALOG_PATH.parent.glob(pattern))

    unique_candidates = sorted({path.resolve() for path in candidates})

    if unique_candidates:
        print("Catalogo de causas cargado por coincidencia:", unique_candidates[0])
        return _read_cause_catalog(unique_candidates[0]), unique_candidates[0]

    available_files = sorted(path.name for path in CAUSE_CATALOG_PATH.parent.iterdir())
    print("No se encontro el catalogo de causas.")
    print("Rutas exactas esperadas:", [str(path) for path in exact_candidates])
    print("Patrones probados:", CAUSE_CATALOG_GLOBS)
    print("Archivos disponibles en data/:", available_files)

    return None, None


def load_valid_geojson():
    last_error = None

    for path in GEOJSON_CANDIDATES:
        if not path.exists():
            continue

        try:
            with path.open(encoding="utf-8") as file:
                geojson_data = json.load(file)
        except Exception as exc:
            last_error = exc
            continue

        if (
            geojson_data.get("type") == "FeatureCollection"
            and geojson_data.get("features")
        ):
            return geojson_data, path

    raise ValueError(
        "No se encontro un archivo GeoJSON valido en la carpeta geojson."
    ) from last_error
