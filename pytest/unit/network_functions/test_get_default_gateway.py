import importlib.util
from pathlib import Path
import subprocess
from unittest.mock import mock_open

import pytest

MODULE_SPEC = importlib.util.spec_from_file_location(
    "test_get_default_gateway_module",
    Path(__file__).resolve().parents[3] / "network_functions" / "get_default_gateway.py",
)
assert MODULE_SPEC and MODULE_SPEC.loader
gateway_module = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(gateway_module)  # type: ignore[union-attr]


def test_get_default_gateway_proc_route(monkeypatch):
    route_data = (
        "Iface\tDestination\tGateway\tFlags\tRefCnt\tUse\tMetric\tMask\tMTU\tWindow\tIRTT\n"
        "eth0\t00000000\t0101A8C0\t0003\t0\t0\t0\t00000000\t0\t0\t0\n"
    )

    monkeypatch.setattr(
        gateway_module.os.path, "exists", lambda path: path == "/proc/net/route"
    )
    monkeypatch.setattr("builtins.open", mock_open(read_data=route_data))
    monkeypatch.setattr(
        gateway_module.subprocess,
        "run",
        lambda *_, **__: pytest.fail("Should not call subprocess when /proc is present"),
    )

    assert gateway_module.get_default_gateway() == "192.168.1.1"


def test_get_default_gateway_ip_route(monkeypatch):
    monkeypatch.setattr(gateway_module.os.path, "exists", lambda _path: False)

    def fake_run(cmd, *_, **__):
        if cmd == ["ip", "route"]:
            return subprocess.CompletedProcess(
                cmd, 0, stdout="default via 10.0.0.1 dev eth0 proto dhcp metric 100\n"
            )
        raise AssertionError("unexpected command")

    monkeypatch.setattr(gateway_module.subprocess, "run", fake_run)

    assert gateway_module.get_default_gateway() == "10.0.0.1"


def test_get_default_gateway_route_get_default(monkeypatch):
    monkeypatch.setattr(gateway_module.os.path, "exists", lambda _path: False)

    def fake_run(cmd, *_, **__):
        if cmd == ["ip", "route"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="default dev eth0 proto kernel\n")
        if cmd == ["route", "-n", "get", "default"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="    gateway: 172.16.0.1\n")
        raise AssertionError("unexpected command")

    monkeypatch.setattr(gateway_module.subprocess, "run", fake_run)

    assert gateway_module.get_default_gateway() == "172.16.0.1"


def test_get_default_gateway_netstat(monkeypatch):
    monkeypatch.setattr(gateway_module.os.path, "exists", lambda _path: False)

    def fake_run(cmd, *_, **__):
        if cmd == ["ip", "route"] or cmd == ["route", "-n", "get", "default"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="")
        if cmd == ["netstat", "-rn"]:
            output = (
                "Routing tables\n\n"
                "Internet:\n"
                "Destination        Gateway            Flags        Refs      Use   Netif Expire\n"
                "default            203.0.113.1        UGSc           3        0     en0\n"
            )
            return subprocess.CompletedProcess(cmd, 0, stdout=output)
        raise AssertionError("unexpected command")

    monkeypatch.setattr(gateway_module.subprocess, "run", fake_run)

    assert gateway_module.get_default_gateway() == "203.0.113.1"


def test_get_default_gateway_no_data(monkeypatch):
    monkeypatch.setattr(gateway_module.os.path, "exists", lambda _path: False)

    def fake_run(cmd, *_, **__):
        raise FileNotFoundError

    monkeypatch.setattr(gateway_module.subprocess, "run", fake_run)

    assert gateway_module.get_default_gateway() == ""
