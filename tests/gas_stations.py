# pylint: disable=C0116,C0114

import pytest

import gas_station_spain as gss


@pytest.mark.parametrize("province_id, name", [(4, "ALMERÍA"), (3, "ALICANTE")])
@pytest.mark.asyncio
async def test_get_by_province(province_id, name):
    gas_stations = await gss.get_gas_stations(province_id=province_id)
    assert len(gas_stations) > 0
    for station in gas_stations:
        assert station.province == name


@pytest.mark.parametrize(
    "province_id, municipality_id, name", [(4, 355, "Rioja"), (3, 256, "San Fulgencio")]
)
@pytest.mark.asyncio
async def test_get_by_municipality(province_id, municipality_id, name):
    gas_stations = await gss.get_gas_stations(
        province_id=province_id, municipality_id=municipality_id
    )
    assert len(gas_stations) > 0
    for station in gas_stations:
        assert station.municipality == name


@pytest.mark.asyncio
async def test_get_by_product():
    province = 20
    products = gss.get_products()
    for product in products:
        gas_stations = await gss.get_gas_stations(
            province_id=province, product_id=product.id
        )
        if len(gas_stations) > 0:
            station = gas_stations[0]
            price = await gss.get_price(station.id, product.id)
            assert price > 0


@pytest.mark.asyncio
async def test_get_provinces():
    provinces = await gss.get_provinces()
    assert len(provinces) > 50
    assert any(p.name == "Almería" for p in provinces)


@pytest.mark.asyncio
async def test_get_municipalities():
    municipalities = await gss.get_municipalities(id_province="04")
    assert len(municipalities) > 100
    assert any(p.name == "Beires" for p in municipalities)


@pytest.mark.asyncio
async def test_get_stations():
    stations = await gss.get_gas_stations(province_id=4, municipality_id=292)
    assert len(stations) > 10
    assert any(p.marquee == "ALCAMPO" for p in stations)


@pytest.mark.asyncio
async def test_get_price():
    price = await gss.get_price(9131, 4)
    assert price > 0.8
