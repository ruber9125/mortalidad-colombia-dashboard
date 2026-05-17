# Mortalidad en Colombia 2019

Aplicacion web construida con Dash y Plotly para explorar registros de mortalidad en Colombia durante 2019. El proyecto carga los microdatos principales, los cruza con DIVIPOLA para enriquecer la ubicacion geografica y genera un dashboard con mapas, series de tiempo, distribuciones por sexo, causas de muerte y grupos de edad.

## Que hace este proyecto

- Carga el dataset principal de mortalidad desde `data/mortalidad_2019.csv`.
- Carga la tabla `DIVIPOLA` desde `data/Divipola_CE_.xlsx`.
- Carga un catalogo de causas de muerte en formato Excel o CSV.
- Valida columnas esperadas antes de procesar la informacion.
- Cruza los registros por `COD_DANE` sin alterar el numero de filas.
- Genera visualizaciones interactivas con Plotly dentro de una app Dash.

## Visualizaciones incluidas

El dashboard muestra:

- Tarjetas resumen con total de defunciones, hombres, mujeres y homicidios de la familia `X95*`.
- Mapa coropletico de muertes por departamento.
- Serie de tiempo de muertes por mes.
- Barras apiladas por departamento y sexo.
- Top 5 ciudades con mas homicidios `X95*`.
- Pie chart con los 10 municipios con menor numero de muertes registradas.
- Tabla con el top 10 de causas de muerte y su descripcion cuando el catalogo esta disponible.
- Histograma por codigo `GRUPO_EDAD1`.

## Datos incluidos

Actualmente el repositorio trae estos archivos base:

- `data/mortalidad_2019.csv`
- `data/Divipola_CE_.xlsx`
- `data/Anexo2.CodigosDeMuerte_CE_15-03-23.csv`
- `geojson/colombia_real.geojson`
- `geojson/colombia.geojson`

En las pruebas locales, el dataset principal contiene `244355` registros y `16` columnas, mientras que `DIVIPOLA` contiene `1123` filas y `6` columnas.

## Requisitos

- Python 3
- `pip`

Dependencias del proyecto:

- `dash`
- `pandas`
- `plotly`
- `openpyxl`
- `gunicorn`

## Instalacion

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecucion local

```powershell
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:8050
```

## Catalogo de causas opcional por variable de entorno

Si quieres usar otro archivo de catalogo de causas, puedes definir `CAUSE_CATALOG_PATH` antes de ejecutar la app:

```powershell
$env:CAUSE_CATALOG_PATH="C:\ruta\al\catalogo.csv"
python app.py
```

Si no defines esa variable, la aplicacion intenta cargar el catalogo desde:

- `data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx`
- `data/Anexo2.CodigosDeMuerte_CE_15-03-23.csv`
- Cualquier archivo de `data/` que coincida con patrones tipo `*CodigosDeMuerte*`

## Estructura del proyecto

```text
mortalidad-colombia/
|-- app.py
|-- requirements.txt
|-- README.md
|-- assets/
|   |-- estilos.css
|   `-- logo_lasalle.png
|-- data/
|   |-- mortalidad_2019.csv
|   |-- Divipola_CE_.xlsx
|   `-- Anexo2.CodigosDeMuerte_CE_15-03-23.csv
|-- geojson/
|   |-- colombia_real.geojson
|   `-- colombia.geojson
`-- src/
    |-- config.py
    |-- loaders.py
    |-- validators.py
    |-- cleaners.py
    |-- helpers.py
    |-- layout.py
    |-- charts/
    `-- services/
```

## Flujo de la app

1. Se cargan datasets y geojson.
2. Se validan las columnas requeridas.
3. Se limpian espacios, nulos y tipos base.
4. Se hace el merge con `DIVIPOLA` usando `COD_DANE`.
5. Se agregan columnas numericas auxiliares para mes y grupo de edad.
6. Se construyen metricas, figuras y tabla final.
7. Dash renderiza el layout completo en una sola vista.

## Modulos principales

- `app.py`: punto de entrada de la aplicacion.
- `src/loaders.py`: carga de CSV, Excel y GeoJSON.
- `src/validators.py`: validaciones de columnas, geojson y merge.
- `src/cleaners.py`: limpieza de datasets.
- `src/services/`: logica de merge, edades, resumen y geo.
- `src/charts/`: generacion de figuras Plotly.
- `src/layout.py`: composicion visual del dashboard.

## Notas utiles

- La app usa `geojson/colombia_real.geojson` como primera opcion y, si no esta disponible, intenta usar `geojson/colombia.geojson`.
- El merge con `DIVIPOLA` esta protegido para evitar perdida o multiplicacion de filas.
- Si el catalogo de causas no se encuentra, la app sigue funcionando, pero la tabla se mostrara sin descripciones enriquecidas.

## Autor

Proyecto desarrollado por Rubert Eduardo Quintero Orozco  
Universidad de La Salle
