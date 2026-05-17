# Mortalidad en Colombia 2019

Dashboard analítico desarrollado con `Python`, `Dash`, `Plotly` y `Pandas` para explorar la mortalidad registrada en Colombia durante 2019. El proyecto usa microdatos del DANE, validación robusta de columnas y merge con DIVIPOLA, integración con GeoJSON y un catálogo CIE-10 para describir causas de muerte.

## Autor

**Rubert Eduardo Quintero Orozco**

Proyecto académico presentado en el contexto de la **Universidad de La Salle**.

## Características

- Visualización del total de muertes por departamento en mapa coroplético.
- Evolución mensual de defunciones en Colombia durante 2019.
- Top de ciudades con mayor concentración de homicidios `X95*`.
- Municipios con menor número de muertes registradas.
- Distribución de muertes por sexo en cada departamento.
- Distribución de muertes por grupo de edad `GRUPO_EDAD1`.
- Tabla de top 10 causas de muerte con descripciones CIE-10.
- Diseño visual profesional, responsive y listo para despliegue en Render.

## Tecnologías

- `Python 3.14`
- `Dash`
- `Plotly`
- `Pandas`
- `openpyxl`
- `gunicorn`

## Estructura del proyecto

```text
mortalidad-colombia/
├── app.py
├── README.md
├── requirements.txt
├── logo_lasalle.png
├── assets/
│   ├── estilos.css
│   └── logo_lasalle.png
├── data/
│   ├── mortalidad_2019.csv
│   ├── Divipola_CE_.xlsx
│   └── Anexo2.CodigosDeMuerte_CE_15-03-23.csv
├── geojson/
│   ├── colombia.geojson
│   └── colombia_real.geojson
└── src/
    ├── __init__.py
    ├── cleaners.py
    ├── config.py
    ├── helpers.py
    ├── layout.py
    ├── loaders.py
    ├── validators.py
    ├── charts/
    │   ├── __init__.py
    │   ├── barras.py
    │   ├── histograma.py
    │   ├── lineas.py
    │   ├── mapa.py
    │   ├── pie.py
    │   ├── stack.py
    │   └── tabla.py
    └── services/
        ├── __init__.py
        ├── age_service.py
        ├── geo_service.py
        ├── merge_service.py
        └── summary_service.py
```

## Arquitectura

- [app.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/app.py): punto de entrada. Orquesta la carga, validación, limpieza, construcción de figuras y layout.
- [src/config.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/config.py): rutas, constantes, textos globales y configuración general.
- [src/loaders.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/loaders.py): carga datasets CSV/Excel, catálogo de causas y GeoJSON.
- [src/cleaners.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/cleaners.py): limpieza robusta de columnas y normalización básica.
- [src/validators.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/validators.py): validaciones de columnas, merge y GeoJSON.
- [src/helpers.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/helpers.py): funciones utilitarias reutilizables.
- [src/layout.py](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/layout.py): composición visual del dashboard.
- [src/charts](C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/charts): un módulo por visualización.
- [src/services](C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/src/services): lógica de apoyo para resumen, edades, merge y geo.

## Fuentes de datos

### 1. Dataset principal

- `data/mortalidad_2019.csv`

Contiene variables como:

- `COD_DANE`
- `COD_DEPARTAMENTO`
- `COD_MUNICIPIO`
- `MES`
- `SEXO`
- `GRUPO_EDAD1`
- `MANERA_MUERTE`
- `COD_MUERTE`

### 2. DIVIPOLA

- `data/Divipola_CE_.xlsx`

Se utiliza para enriquecer el dataset principal con:

- `DEPARTAMENTO`
- `MUNICIPIO`

### 3. Catálogo de causas CIE-10

- `data/Anexo2.CodigosDeMuerte_CE_15-03-23.csv`

Se usa para traducir `COD_MUERTE` a descripciones clínicas. El sistema intenta primero por código de 4 caracteres y, si no encuentra coincidencia, hace fallback al código de 3 caracteres.

### 4. GeoJSON de Colombia

- `geojson/colombia_real.geojson`
- `geojson/colombia.geojson`

Se utiliza para el mapa coroplético de mortalidad por departamento.

## Validaciones implementadas

- Validación de columnas esperadas en el dataset principal.
- Validación de columnas esperadas en DIVIPOLA.
- Limpieza con `fillna("")`, `astype(str)` y `strip()`.
- Merge con `validate="many_to_one"`.
- Verificación de que el merge no agregue ni elimine filas.
- Validación de la propiedad `DPTO` en el GeoJSON.
- Diagnóstico por consola de columnas, longitud del merge y cobertura del mapa.

## Ejecución local

Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecuta la aplicación:

```bash
python app.py
```

En local abre:

```text
http://127.0.0.1:8050/
```

## Despliegue en Render

La aplicación expone:

```python
server = app.server
```

Comando recomendado:

```bash
gunicorn app:server
```

## Dependencias

El archivo [requirements.txt](/C:/Users/RUBERT_PC/Desktop/mortalidad-colombia/requirements.txt) incluye:

```text
dash==4.1.0
pandas==3.0.2
plotly==6.7.0
openpyxl==3.1.5
gunicorn
```

## Visualizaciones incluidas

- **Mapa coroplético**: total de muertes por departamento.
- **Línea temporal**: total de muertes por mes.
- **Barras de homicidios**: top de ciudades con mayor número de homicidios `X95*`.
- **Pie chart**: municipios con menor número de muertes registradas.
- **Barras apiladas por sexo**: distribución de hombres y mujeres por departamento.
- **Histograma**: distribución de muertes por grupo de edad.
- **Tabla de causas**: top 10 causas con descripción CIE-10.

## Notas importantes

- El proyecto está modularizado y no depende de un único `app.py` monolítico.
- El catálogo de causas ya no es opcional para la tabla principal si quieres descripciones completas.
- El dashboard está pensado para fines analíticos, académicos y de presentación profesional.

## Estado actual

El proyecto se encuentra:

- modularizado
- funcional
- visualmente profesional
- compatible con Render
- listo para seguir mejorando visualizaciones y narrativa analítica
