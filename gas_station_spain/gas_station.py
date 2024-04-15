from dataclasses import dataclass

import aiohttp

from .const import GAS_STATION_ENDPOINT, GAS_STATION_PRICE_ENDPOINT


@dataclass
class Product:
    id: int
    name: str
    code: str


PRODUCTS = {
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


class GasStation:
    def __init__(self, data):
        self.id = data['id']
        self.marquee = data['rotulo']
        self.address = data['direccion']
        self.province = data['provincia']
        self.latitude = data['coordenadaY_dec']
        self.longitude = data['coordenadaX_dec']
        self.municipality = data['localidad'].strip().title()


async def get_gas_stations(
        province_id: int | None = None,
        municipality_id: int | None = None,
        product_id: int | None = None
):
    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.post(GAS_STATION_ENDPOINT, json={
        "tipoEstacion": "EESS",
        "idProvincia": province_id,
        "idMunicipio": municipality_id,
        "idProducto": product_id
    })

    data = await response.json()
    await session.close()
    return [GasStation(s['estacion']) for s in data['estaciones']]


async def get_price(station_id, product_id):
    headers = {"Accept": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    response = await session.get(GAS_STATION_PRICE_ENDPOINT.format(station_id))
    data = await response.json()
    product = PRODUCTS[product_id]
    await session.close()
    return data[f"precio{product.code}"]


def get_products() -> list[Product]:
    return list(PRODUCTS.values())
