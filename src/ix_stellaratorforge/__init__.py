
"""IX-StellaratorForge reactor-design layer built on the preserved IX-Fusion scientific foundation."""

from .physics import (
    DTReactionLedger,
    PlasmaScreeningLedger,
    PowerBalance,
    dt_reaction_ledger,
    ecrh_frequency_ghz,
    plasma_screening_ledger,
    power_balance,
)
from .reactor import ReactorConfig, ReactorValidation, load_reactor_config, validate_reactor_config
from .sfr2 import geometry_from_sector_lengths, run_sfr2_screen, validate_sfr2_config
from .sfr2_actuation import run_actuation_overlay_screen, validate_actuation_config
from .sfr3_field_integrity import (
    build_response_matrix,
    run_sfr3_field_integrity_screen,
    validate_sfr3_config,
)
from .sfr3_dual_boundary import (
    run_dual_boundary_screen,
    validate_dual_boundary_config,
)
from .sfr4_integrated_campaign import (
    run_integrated_campaign,
    validate_integrated_config,
)

__all__ = [
    "DTReactionLedger",
    "PlasmaScreeningLedger",
    "PowerBalance",
    "ReactorConfig",
    "ReactorValidation",
    "dt_reaction_ledger",
    "ecrh_frequency_ghz",
    "load_reactor_config",
    "plasma_screening_ledger",
    "power_balance",
    "validate_reactor_config",
    "geometry_from_sector_lengths",
    "run_sfr2_screen",
    "run_actuation_overlay_screen",
    "build_response_matrix",
    "run_sfr3_field_integrity_screen",
    "run_dual_boundary_screen",
    "validate_actuation_config",
    "validate_sfr2_config",
    "validate_sfr3_config",
    "validate_dual_boundary_config",
    "run_integrated_campaign",
    "validate_integrated_config",
]
