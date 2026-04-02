# pylint: disable=C0116,C0114
"""Tests for server error handling with mocked responses."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

import gas_station_spain_api as gss


@pytest.mark.asyncio
async def test_get_gas_stations_server_error_500():
    """Test that get_gas_stations raises GasStationServerUnavailableException on 500 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup async methods
        mock_session.post = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        # Test that it raises the exception (tenacity will retry but will keep getting 500)
        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_gas_stations(province_id=4)

        assert exc_info.value.status_code == 500
        assert "500" in str(exc_info.value)
        # Due to retries (3 attempts), close should be called 3 times
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_gas_stations_server_error_502():
    """Test that get_gas_stations raises GasStationServerUnavailableException on 502 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 502

        # Setup async methods
        mock_session.post = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_gas_stations(province_id=4)

        assert exc_info.value.status_code == 502
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_gas_stations_server_error_503():
    """Test that get_gas_stations raises GasStationServerUnavailableException on 503 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 503

        # Setup async methods
        mock_session.post = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_gas_stations(province_id=4)

        assert exc_info.value.status_code == 503
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_price_server_error_500():
    """Test that get_price raises GasStationServerUnavailableException on 500 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup async methods
        mock_session.get = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_price(station_id=9131, product_id=4)

        assert exc_info.value.status_code == 500
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_gas_station_server_error_500():
    """Test that get_gas_station raises GasStationServerUnavailableException on 500 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup async methods
        mock_session.get = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_gas_station(station_id=9131)

        assert exc_info.value.status_code == 500
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_provinces_server_error_500():
    """Test that get_provinces raises GasStationServerUnavailableException on 500 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup async methods
        mock_session.get = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_provinces()

        assert exc_info.value.status_code == 500
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_municipalities_server_error_500():
    """Test that get_municipalities raises GasStationServerUnavailableException on 500 error."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 500

        # Setup async methods
        mock_session.post = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        with pytest.raises(gss.GasStationServerUnavailableException) as exc_info:
            await gss.get_municipalities(id_province="04")

        assert exc_info.value.status_code == 500
        assert mock_session.close.call_count == 3


@pytest.mark.asyncio
async def test_get_gas_stations_success_with_mock():
    """Test that get_gas_stations works correctly with a successful mocked response."""

    with patch(
        "gas_station_spain_api.gas_station._create_session"
    ) as mock_create_session:
        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "estaciones": [
                    {
                        "estacion": {
                            "id": 1234,
                            "rotulo": "TEST STATION",
                            "direccion": "Test Address",
                            "provincia": "ALMERÍA",
                            "coordenadaY_dec": 36.840,
                            "coordenadaX_dec": -2.467,
                            "localidad": "Test City",
                        }
                    }
                ]
            }
        )

        # Setup async methods
        mock_session.post = AsyncMock(return_value=mock_response)
        mock_session.close = AsyncMock()
        mock_create_session.return_value = mock_session

        # Call the function
        stations = await gss.get_gas_stations(province_id=4)

        # Assertions
        assert len(stations) == 1
        assert stations[0].id == 1234
        assert stations[0].marquee == "Test Station"
        assert stations[0].province == "ALMERÍA"
        mock_session.close.assert_called_once()
