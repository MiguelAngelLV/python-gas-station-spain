# Python Gas Station Spain

### Descripción

Esta es una biblioteca para obtener el precio actual del combustible en las distintas gasolineras españolas.

### Fuente de datos

Los datos son extraídos de de la API oficial del estado: [Geoportal Gasolineras](https://geoportalgasolineras.es/geoportal-instalaciones/Inicio).

Desgraciadamente, el servicio no es muy estable y es posible que ocurran errores de conexión

### Uso

```python

import gas_station_spain_api as gss

# Obtener listado de provincias
provinces = await gss.get_provinces()

# Obtener listado de municipios
municipalities = await gss.get_municipalities(provinces[0].id)

# Obtener estaciones de una provincia
p1_gas_stations = await gss.get_gas_stations(province_id=provinces[1].id)

# Obtener estaciones de un municipio
m1_gas_stations = await gss.get_gas_stations(provinces[0].id, municipalities[0].id)
```
