from __future__ import annotations

from om1.inputs.system_monitor import SystemMonitorConfig, SystemMonitorInput


def test_system_monitor_mock_mode_returns_expected_keys() -> None:
    """SystemMonitorInput in mock mode returns all expected metric keys."""
    config = SystemMonitorConfig(mock_mode=True)
    sensor = SystemMonitorInput(config=config)

    metrics = sensor.read()

    assert isinstance(metrics, dict)
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_percent" in metrics

    for key in ("cpu_percent", "memory_percent", "disk_percent"):
        value = metrics[key]
        assert isinstance(value, float)
        assert 0.0 <= value <= 100.0


def test_system_monitor_mock_mode_custom_values() -> None:
    """SystemMonitorInput mock mode respects custom configured percentages."""
    config = SystemMonitorConfig(
        mock_mode=True,
        cpu_percent=10.0,
        memory_percent=20.0,
        disk_percent=30.0,
    )
    sensor = SystemMonitorInput(config=config)

    metrics = sensor.read()

    assert metrics["cpu_percent"] == 10.0
    assert metrics["memory_percent"] == 20.0
    assert metrics["disk_percent"] == 30.0
