from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnergyLedger:
    fusion_power: float | None = None
    external_heating_power: float | None = None
    magnet_power: float | None = None
    cryogenic_power: float | None = None
    pumping_power: float | None = None
    rf_power: float | None = None
    thermal_conversion_efficiency: float | None = None

    def missing_terms(self) -> tuple[str, ...]:
        missing = []
        for name, value in self.__dict__.items():
            if value is None:
                missing.append(name)
        return tuple(missing)

    def net_electric_power(self) -> float:
        missing = self.missing_terms()
        if missing:
            raise ValueError("net electric power is UNKNOWN; missing terms: " + ", ".join(missing))
        assert self.fusion_power is not None
        assert self.external_heating_power is not None
        assert self.magnet_power is not None
        assert self.cryogenic_power is not None
        assert self.pumping_power is not None
        assert self.rf_power is not None
        assert self.thermal_conversion_efficiency is not None
        generated = self.fusion_power * self.thermal_conversion_efficiency
        recirculating = (
            self.external_heating_power
            + self.magnet_power
            + self.cryogenic_power
            + self.pumping_power
            + self.rf_power
        )
        return generated - recirculating
