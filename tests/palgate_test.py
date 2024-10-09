import json

import pytest
from pytest_mock import MockerFixture

from palgate_py.palgate.config import Config, User
from palgate_py.palgate.palgate import PalGate


@pytest.fixture(scope="session")
def palgate_instance():
    """Sets up a palgate for the session that can be reused.
    We need it scoped to session so we reuse the JVM and avoid starting it multiple times."""

    return PalGate()


@pytest.fixture
def palgate(palgate_instance):
    """Sets up a palgate instance with a default configuration and user."""

    palgate_instance.config = Config()
    palgate_instance.config.user = User(
        id="123", token="abcdef", firstname="John", lastname="Doe", image=False
    )
    return palgate_instance


def test_api(mocker: MockerFixture, palgate):
    mocker.patch(
        "palgate_py.palgate.palgate.PalGate._get_token", return_value="mock_token"
    )
    mocker.patch(
        "palgate_py.palgate.palgate.request.urlopen",
        mocker.mock_open(read_data=json.dumps({"status": "ok"}).encode()),
    )

    response = palgate._api("test/path")  # noqa: SLF001
    assert response == {"status": "ok"}


def test_int_to_hex_string(palgate):
    result = palgate.int_to_hex_string([255, 0, 128])
    assert result == "FF0080"


def test_hex_string_to_byte_array(palgate):
    result = palgate.hex_string_to_byte_array("FF0080")
    assert result == bytearray([255, 0, 128])


def test_login(mocker: MockerFixture, palgate):
    mocker.patch(
        "palgate_py.palgate.palgate.PalGate._api",
        return_value={"user": palgate.config.user._asdict()},
    )
    error, msg = palgate.login()
    assert not error
    assert msg is None
    assert palgate.config.user.id == "123"
    assert palgate.config.user.token == "abcdef"


def test_is_token_valid(mocker: MockerFixture, palgate):
    mocker.patch(
        "palgate_py.palgate.palgate.PalGate._api", return_value={"status": "ok"}
    )
    error, msg = palgate.is_token_valid()
    assert not error
    assert msg == ""


def test_list_devices(mocker: MockerFixture, palgate):
    mocker.patch(
        "palgate_py.palgate.palgate.PalGate._api",
        return_value={"devices": [{"id": "1", "name": "Device1"}]},
    )
    devices = palgate.list_devices()
    assert len(devices) == 1
    assert devices[0].id == "1"
    assert devices[0].name == "Device1"


def test_open_gate(mocker: MockerFixture, palgate):
    mocker.patch(
        "palgate_py.palgate.palgate.PalGate._api", return_value={"status": "ok"}
    )
    error, msg = palgate.open_gate("device_id")
    assert not error
    assert msg == ""


def test_logout(palgate):
    palgate.logout()
    assert palgate.config.palgate is None