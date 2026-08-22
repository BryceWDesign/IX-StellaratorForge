# SFR-3 Field Integrity Shell bill of materials

`SFR3_FIELD_INTEGRITY_SHELL_BOM.csv` is a 52-row architecture inventory. It is not a procurement list and does not assert dimensions, prices, operating lifetime or supplier qualification.

## Design decision

The only entries that directly create confinement fields are the primary coils, active trim coils, passive superconducting loops when responding to changing flux, and the deferred permanent-magnet option. Walls, liquids, shielding and damping hardware may protect or preserve the magnetic system but receive zero direct confinement credit.

The baseline branch uses:

- steady copper-stabilized REBCO primary coils;
- 24 individually driven correction channels;
- 24 passive superconducting loops as a research option for transient errors only;
- independent magnetic, current, quench, strain and support-motion observability;
- fail-closed resource-gated control;
- warm-side structural-mode suppression;
- WC/B4C shielding with HfH composite retained only as a solver-dependent local option;
- segmented tungsten-family plasma-facing components; and
- the existing PbLi / RAFM / SiC-or-alumina blanket family.

## Excluded combinations

Diamond, glitter, passive dense liquids and a flexible pressure-driven vessel are explicitly rejected as confinement mechanisms. Liquid lithium is retained only as a controlled divertor or edge-conditioning experiment. An imploding lithium liner belongs to a separate pulsed magnetized-target-fusion machine and is not merged into SFR-3.

Every `NEW`, `DEFER` or `SEPARATE` row has a named qualification requirement. No row closes a physical fusion gate by inclusion in this BOM.
