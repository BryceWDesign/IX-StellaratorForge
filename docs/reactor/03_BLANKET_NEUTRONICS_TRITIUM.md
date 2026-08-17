
# Blanket, Neutronics and Tritium

## Reference breeder branch

Rev A carries a **reference** liquid PbLi breeder branch with enriched lithium-6 and helium heat removal because it allows one integrated calculation to address tritium production, neutron energy deposition and primary heat extraction. The material choice is not frozen: corrosion, MHD pressure drop, structural compatibility, tritium permeation, safety and maintenance can eliminate it.

An alternate breeder branch is mandatory before design down-selection so the reactor is not trapped by one material assumption.

## Required G7 neutronics outputs

A 3-D CAD-aware OpenMC/DAGMC or equivalent analysis must calculate:

- local and global TBR;
- TBR loss from ECRH, diagnostic, fueling, vacuum and maintenance penetrations;
- neutron and photon heating by component;
- peak nuclear heating in HTS and cryogenic structures;
- displacement/damage and helium-production proxies tied to selected materials;
- streaming hot spots through seams and penetrations;
- activation and shutdown dose inputs for remote maintenance;
- energy multiplication and spatial heat-deposition maps.

No homogenized radial model can promote G7 by itself.

## Tritium rule

SFR-1 uses:

- design target: full-3D TBR ≥1.15;
- hard floor: TBR ≥1.10 after realistic penetrations in the committed reference state;
- startup inventory target: ≤2 kg;
- explicit fuel-processing time and inventory accounting before any self-sufficiency claim.

A TBR above one is necessary but not sufficient for tritium self-sufficiency. Processing losses, reserve inventory, radioactive decay, extraction time and plant availability must be included in G8.

## D-T burn ledger

At the 1 GW fusion-power design target, the exact D-T reaction-energy calculation consumes about 0.153 kg of tritium per day and 0.102 kg of deuterium per day if 1 GW fusion power were sustained continuously. This is a useful fuel-cycle scale, not evidence that SFR-1 can achieve that burn.
