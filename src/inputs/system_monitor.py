from __future__ import annotations

import logging
from typing import Dict, Optional

from pydantic import BaseModel, Field

try:  # pragma: no cover - import guard
    import psutil

    _PSUTIL_AVAILABLE = True
except Exception:  # pragma: no cover - defensive
    psutil = None  # type: ignore[assignment]
    _PSUTIL_AVAILABLE = False

logger = logging.getLogger(__name__)


class SystemMonitorConfig(BaseModel):
    """Configuration for the SystemMonitor input.

    Attributes:
        mock_mode: When True, the monitor returns fake but realistic values.
        cpu_percent: Optional fixed CPU percentage when in mock mode.
        memory_percent: Optional fixed memory percentage when in mock mode.
        disk_percent: Optional fixed disk percentage when in mock mode.
    """

    mock_mode: bool = Field(default=False)
    cpu_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    memory_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    disk_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0)


class SystemMonitorInput:
    """System resource monitor input plugin.

    This input provides system resource utilization metrics, including CPU,
    RAM, and disk usage percentages. It supports a mock mode for CI, unit
    tests, and environments where ``psutil`` is not available.
    """

    def __init__(self, config: SystemMonitorConfig) -> None:
        """Initialize the system monitor input.

        Args:
            config: Configuration for the system monitor.
        """
        self._config = config
        self._mock_mode = config.mock_mode or not _PSUTIL_AVAILABLE

        if not _PSUTIL_AVAILABLE:
            logger.warning(
                "psutil is not available; SystemMonitorInput will run in mock mode.",
            )

        if self._mock_mode:
            logger.info("SystemMonitorInput initialized in mock mode.")
        else:
            logger.info("SystemMonitorInput initialized in real mode using psutil.")

    def _mock_metrics(self) -> Dict[str, float]:
        """Generate fake but realistic system resource metrics.

        Returns:
            A dictionary with CPU, memory, and disk usage percentages.
        """
        cpu = self._config.cpu_percent if self._config.cpu_percent is not None else 45.0
        memory = (
            self._config.memory_percent
            if self._config.memory_percent is not None
            else 60.0
        )
        disk = (
            self._config.disk_percent
            if self._config.disk_percent is not None
            else 70.0
        )

        logger.debug(
            "Mock metrics generated: cpu_percent=%s, memory_percent=%s, "
            "disk_percent=%s",
            cpu,
            memory,
            disk,
        )

        return {
            "cpu_percent": float(cpu),
            "memory_percent": float(memory),
            "disk_percent": float(disk),
        }

    def _real_metrics(self) -> Dict[str, float]:
        """Collect real system resource metrics using psutil.

        Returns:
            A dictionary with CPU, memory, and disk usage percentages.
        """
        if not _PSUTIL_AVAILABLE or psutil is None:
            logger.error(
                "psutil is not available; falling back to mock metrics in "
                "SystemMonitorInput.",
            )
            return self._mock_metrics()

        cpu_percent = psutil.cpu_percent(interval=None)
        virtual_mem = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")

        logger.debug(
            "Real metrics collected: cpu_percent=%s, memory_percent=%s, "
            "disk_percent=%s",
            cpu_percent,
            virtual_mem.percent,
            disk_usage.percent,
        )

        return {
            "cpu_percent": float(cpu_percent),
            "memory_percent": float(virtual_mem.percent),
            "disk_percent": float(disk_usage.percent),
        }

    def read(self) -> Dict[str, float]:
        """Read a snapshot of system resource utilization.

        Returns:
            A dictionary with keys ``cpu_percent``, ``memory_percent``, and
            ``disk_percent``, each mapped to a floating point percentage value.
        """
        if self._mock_mode:
            return self._mock_metrics()

        return self._real_metrics()
