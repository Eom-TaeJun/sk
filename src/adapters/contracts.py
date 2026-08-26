from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


class Sensor(Protocol):
    def collect(self) -> dict[str, Any]: ...


class DemandMemorySensor(Sensor, Protocol):
    pass


class SupplyInfraSensor(Sensor, Protocol):
    pass


class CommercialPolicySensor(Sensor, Protocol):
    pass


class AuditorSensor(Sensor, Protocol):
    pass


class AgentAdapter(ABC):
    """Boundary between non-deterministic orchestration and the Core Harness."""

    @abstractmethod
    def normalized_payload(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True)
class ManualScenarioAdapter(AgentAdapter):
    payload: dict[str, Any]

    def normalized_payload(self) -> dict[str, Any]:
        return self.payload
