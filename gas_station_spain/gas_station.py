"""Gas Station Spain"""

from dataclasses import dataclass

import aiohttp
import tenacity
from tenacity import stop_after_attempt, wait_fixed

_STATIONS_ENDPOINT = "https://geoportalgasolineras.es/geoportal/rest/busquedaEstaciones"
_STATION_ENDPOINT = (
    "https://geoportalgasolineras.es/geoportal/rest/{}/busquedaEstacionPrecio"
)
_PROVINCES_ENDPOINT = "https://geoportalgasolineras.es/geoportal/rest/getProvincias"
_MUNICIPALITIES_ENDPOINT = (
    "https://geoportalgasolineras.es/geoportal/rest/getMunicipios"
)


@dataclass
class Product:
    """Product."""

    id: int
    name: str
    code: str


@dataclass
class Province:
    """Province."""

    id: str
    name: str


@dataclass
class Municipality:
    """Municipality."""

    id: str
    name: str


_PRODUCTS = {
    1: Product(id=1, name="Gasolina 95 E5", code="Gasolina95E5"),
    3: Product(id=3, name="Gasolina 98 E5", code="Gasolina98E5"),
    4: Product(id=4, name="Gasóleo A", code="GasoleoA"),
    5: Product(id=5, name="Gasóleo Premium", code="GasoleoPremium"),
    6: Product(id=6, name="Gasóleo B", code="GasoleoB"),
    7: Product(id=7, name="Gasóleo C", code="GasoleoC"),
    8: Product(id=8, name="Biodiesel", code="Biodiesel"),
    16: Product(id=16, name="Bioetanol", code="Biotanol"),
    17: Product(id=17, name="Gases licuados del petróleo", code="GasesLicuados"),
    18: Product(id=18, name="Gas natural comprimido", code="GasNatComp"),
    19: Product(id=19, name="Gas natural licuado", code="GasNatLicuado"),
    20: Product(id=20, name="Gasolina 95 E5 Premium", code="Gasolina95E5Premium"),
    21: Product(id=21, name="Gasolina 98 E10", code="Gasolina98E10"),
    23: Product(id=23, name="Gasolina 95 E10", code="Gasolina95E10"),
}


@dataclass
class GasStation:
    """Gas Station Information."""

    id: int
    marquee: str
    address: str
    province: str
    latitude: float
    longitude: float
    municipality: str

    @staticmethod
    def from_list(data: dict) -> "GasStation":
        """Create GasStation from a dictionary."""
        return GasStation(
            id=data["id"],
            marquee=data["rotulo"].title(),
            address=data["direccion"],
            province=data["provincia"],
            latitude=data["coordenadaY_dec"],
            longitude=data["coordenadaX_dec"],
            municipality=data["localidad"].strip().title(),
        )

    @staticmethod
    def from_individual(data: dict) -> "GasStation":
        """Create GasStation from a dictionary."""
        return GasStation(
            id=data["eessId"],
            marquee=data["rotulo"].title(),
            address=data["direccion"],
            province=data["provincia"],
            latitude=data["coordenadaY"],
            longitude=data["coordenadaX"],
            municipality=data["localidad"].strip().title(),
        )


@tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_gas_stations(
    province_id: int | None = None,
    municipality_id: int | None = None,
    product_id: int | None = None,
) -> list[GasStation]:
    """Get gas stations with optionals filters."""

    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.post(
        _STATIONS_ENDPOINT,
        json={
            "tipoEstacion": "EESS",
            "idProvincia": province_id,
            "idMunicipio": municipality_id,
            "idProducto": product_id,
        },
    )

    data = await response.json()
    await session.close()
    return [GasStation.from_list(s["estacion"]) for s in data["estaciones"]]


@tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_price(station_id, product_id) -> float:
    """Get the actual product price in selected station."""

    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.get(_STATION_ENDPOINT.format(station_id))
    data = await response.json()
    product = _PRODUCTS[product_id]
    await session.close()
    return data[f"precio{product.code}"]


@tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_gas_station(station_id) -> GasStation:
    """Get gas station by id."""

    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.get(_STATION_ENDPOINT.format(station_id))
    data = await response.json()
    await session.close()
    return GasStation.from_individual(data)


def get_products() -> list[Product]:
    """Get product list."""
    return list(_PRODUCTS.values())


@tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_provinces() -> list[Province]:
    """Get provinces list."""

    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.get(_PROVINCES_ENDPOINT)
    data = await response.json()
    await session.close()
    return [Province(id=p["id"], name=p["nombre"].title()) for p in data["provincias"]]


@tenacity.retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_municipalities(id_province: str) -> list[Municipality]:
    """Get municipalities list."""

    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.post(
        _MUNICIPALITIES_ENDPOINT, data={"idProvincia": id_province}
    )
    data = await response.json()
    await session.close()
    return [Municipality(id=p["id"], name=p["desMunicipio"]) for p in data]
