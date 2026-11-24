"""portscan.presets için birim testleri."""

import pytest

from portscan.presets import PRESETS, describe_presets, get_preset


@pytest.mark.parametrize("name", sorted(PRESETS))
def test_presets_are_sorted_unique_and_valid(name):
    ports = get_preset(name)

    assert ports, f"{name} boş olmamalı"
    assert ports == sorted(set(ports))
    assert all(1 <= port <= 65535 for port in ports)


def test_top100_has_exactly_100_ports():
    assert len(get_preset("top100")) == 100


def test_get_preset_returns_a_copy():
    ports = get_preset("web")
    ports.append(1)
    assert 1 not in get_preset("web")


def test_udp_preset_contains_common_services():
    ports = get_preset("udp")

    assert 53 in ports   # DNS
    assert 123 in ports  # NTP
    assert 161 in ports  # SNMP


def test_get_preset_unknown_raises():
    with pytest.raises(ValueError):
        get_preset("yok-boyle-bir-liste")


def test_describe_presets():
    described = describe_presets()
    assert set(described) == set(PRESETS)
    assert described["top100"] == 100
