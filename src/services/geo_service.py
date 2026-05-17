from src.config import FEATURE_ID_COLUMN
from src.validators import validate_geojson_feature_id


def get_geojson_properties(geojson_data):
    return list(geojson_data["features"][0].get("properties", {}).keys())


def get_geojson_department_codes(geojson_data):
    properties = get_geojson_properties(geojson_data)
    validate_geojson_feature_id(properties)

    return {
        str(feature["properties"][FEATURE_ID_COLUMN]).zfill(2)
        for feature in geojson_data["features"]
    }
