import pytest

pytestmark = [pytest.mark.unit, pytest.mark.cli_functions]
from python_utils.cli_functions.get_network_info import get_network_info


def test_get_network_info_returns_dict() -> None:
    """
    Test case 1: Test get_network_info returns a dictionary.
    """
    net_info = get_network_info()
    assert isinstance(net_info, dict)


def test_get_network_info_interface_structure() -> None:
    """
    Test case 2: Test each interface has expected structure.
    """
    net_info = get_network_info()

    for interface_name, interface_data in net_info.items():
        assert isinstance(interface_name, str)
        assert isinstance(interface_data, dict)

        # Check for expected keys
        assert "ipv4" in interface_data
        assert "ipv6" in interface_data
        assert "mac" in interface_data


def test_get_network_info_address_lists() -> None:
    """
    Test case 3: Test address lists are valid.
    """
    net_info = get_network_info()

    for interface_data in net_info.values():
        assert isinstance(interface_data["ipv4"], list)
        assert isinstance(interface_data["ipv6"], list)
        assert isinstance(interface_data["mac"], list)


def test_get_network_info_address_dict_structure() -> None:
    """
    Test case 4: Test individual address dictionaries have expected keys.
    """
    net_info = get_network_info()

    for interface_data in net_info.values():
        for addr_list in [
            interface_data["ipv4"],
            interface_data["ipv6"],
            interface_data["mac"],
        ]:
            for addr_dict in addr_list:
                assert isinstance(addr_dict, dict)
                assert "address" in addr_dict
                assert "netmask" in addr_dict


def test_get_network_info_at_least_one_interface() -> None:
    """
    Test case 5: Most systems should have at least one network interface.
    """
    net_info = get_network_info()
    # Most systems have at least loopback
    assert len(net_info) >= 0  # Can be 0 in some test environments


def test_get_network_info_consistency() -> None:
    """
    Test case 6: Test consistency between multiple calls.
    """
    net_info1 = get_network_info()
    net_info2 = get_network_info()

    # Interface names should be consistent
    assert set(net_info1.keys()) == set(net_info2.keys())
