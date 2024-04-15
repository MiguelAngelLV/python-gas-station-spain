import pytest

from gas_station_spain.gas_station import get_gas_stations, get_price, get_products


@pytest.mark.parametrize(
    "province_id, name",
    [
        (4, "ALMERÍA"),
        (3, "ALICANTE")
    ])
@pytest.mark.asyncio
async def test_get_by_province(province_id, name):
    gas_stations = await get_gas_stations(province_id=province_id)
    assert len(gas_stations) > 0
    for station in gas_stations:
        assert station.province == name


@pytest.mark.parametrize(
    "province_id, municipality_id, name",
    [
        (4, 355, "Rioja"),
        (3, 270, "Tormos")
    ])
@pytest.mark.asyncio
async def test_get_by_municipality(province_id, municipality_id, name):
    gas_stations = await get_gas_stations(province_id=province_id, municipality_id=municipality_id)
    assert len(gas_stations) > 0
    for station in gas_stations:
        assert station.municipality == name


@pytest.mark.asyncio
async def test_get_by_product():
    province = 20
    products = get_products()
    for product in products:
        gas_stations = await get_gas_stations(province_id=province, product_id=product.id)
        if len(gas_stations) > 0:
            station = gas_stations[0]
            price = await get_price(station.id, product.id)
            assert price > 0
