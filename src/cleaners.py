from src.config import EXPECTED_DIVIPOLA_COLUMNS, EXPECTED_MAIN_COLUMNS


def clean_expected_columns(frame, expected_columns):
    cleaned = frame.copy()

    for column in expected_columns:
        cleaned[column] = cleaned[column].fillna("").astype(str).str.strip()

    return cleaned


def clean_main_dataset(frame):
    return clean_expected_columns(frame, EXPECTED_MAIN_COLUMNS)


def clean_divipola_dataset(frame):
    return clean_expected_columns(frame, EXPECTED_DIVIPOLA_COLUMNS)


def clean_cause_catalog(catalog):
    if catalog is None:
        return None

    cleaned = catalog.copy()
    cleaned.columns = cleaned.columns.str.strip()

    for column in cleaned.columns:
        cleaned[column] = cleaned[column].fillna("").astype(str).str.strip()

    return cleaned
