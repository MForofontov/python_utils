from linux_functions.get_network_interfaces import get_network_interfaces


def test_get_network_interfaces_returns_dict() -> None:
    """
    Test case 1: Test get_network_interfaces function returns a dictionary.
    """
    interfaces: dict = get_network_interfaces()
    assert isinstance(interfaces, dict)


def test_get_network_interfaces_has_loopback() -> None:
    """
    Test case 2: Test get_network_interfaces function includes loopback interface.
    """
    interfaces: dict = get_network_interfaces()
    # Most systems have a loopback interface
    # This might be 'lo', 'lo0', or similar depending on the system
    loopback_found: bool = any("lo" in iface.lower() for iface in interfaces.keys())
    assert loopback_found


def test_get_network_interfaces_structure() -> None:
    """
    Test case 3: Test get_network_interfaces function returns properly structured data.
    """
    interfaces: dict = get_network_interfaces()

    for interface_name, interface_data in interfaces.items():
        assert isinstance(interface_name, str)
        # Accept list of snicaddr objects or similar structure
        assert isinstance(interface_data, (list, tuple)), f"Expected list/tuple, got {type(interface_data).__name__}"
        # Optionally check that each item is an address object (has 'address' attribute)
        for addr in interface_data:
            assert hasattr(addr, "address"), f"Item missing 'address' attribute: {addr}"
