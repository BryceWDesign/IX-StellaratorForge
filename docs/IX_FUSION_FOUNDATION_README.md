# IX-Fusion v0.2.0-vNext

> **vNext research branch:** The original v0.1.0 reduced-order result remains `FAIL_OR_INCONCLUSIVE`. This branch does not overwrite that evidence. It adds a multi-family, multi-fidelity promotion architecture so C6, 3FP/4FP/6FP QI/QI-pwO candidates, a QA engineering reference, and a direct-orbit assumption-breaker can compete under the same solver-authority gates.
>
> Start with [`docs/vnext/00_VNEXT_SCIENTIFIC_THESIS.md`](docs/vnext/00_VNEXT_SCIENTIFIC_THESIS.md) and run `python check_vnext.py`.

---

## v0.1.0 baseline documentation (retained)

# IX-Fusion

**Evaluation-only computational research framework for falsifiable stellarator hypothesis testing.**

[![Quality Gate](https://github.com/BryceWDesign/IX-Fusion/actions/workflows/quality.yml/badge.svg)](https://github.com/BryceWDesign/IX-Fusion/actions/workflows/quality.yml)

IX-Fusion asks whether a **C6-seeded quasi-isodynamic / omnigenous stellarator starting
condition** is worth pursuing once magnetic, particle-confinement, active-control, structural,
and reactor-facing engineering penalties are evaluated against matched controls.

The project is not built around preserving a symbol. The C6 / inverted-Flower geometry is
only the historical source of the initial six-field-period hypothesis. Physics is allowed to
modify or reject it.

> **Current release verdict:** `FAIL_OR_INCONCLUSIVE` at the reduced-model gate.  
> **Scientific stage:** `geometry_hypothesis`.  
> IX-Fusion does **not** claim demonstrated plasma confinement, ignition, net energy, net
> electricity, or reactor feasibility.

## Current proof-of-concept result

Release 0.1 compares the C6 seed with a matched five-field-period helical control using the
same deterministic optimization budget.

| Reduced-order metric | C6 candidate | Matched control | C6 outcome |
|---|---:|---:|---|
| Composite screening objective — lower is better | 0.0318820 | 0.0304006 | **4.87% worse** |
| Bounce-action variation proxy — lower is better | 0.000258110 | 0.000257673 | **0.17% worse** |
| Mean radial-excursion proxy — lower is better | 0.00930135 | 0.0130368 | **28.65% better** |
| Field-line escape fraction in tested reduced set | 0 | 0 | tie |
| Engineering burden proxy — lower is better | 0.870566 | 0.788074 | **10.47% worse** |

The C6 candidate therefore **does not clear the predeclared overall advantage gate**, even
though one field-line metric is favorable. That distinction is intentional: IX-Fusion is
designed so one attractive number cannot override contrary evidence.

See [`PROOF_OF_CONCEPT.md`](PROOF_OF_CONCEPT.md) and
[`results/poc/POC_RESULT.md`](results/poc/POC_RESULT.md).

![Reduced-order comparison](results/figures/poc_metric_comparison.png)

## Research question

> **Does a C6-seeded quasi-isodynamic/omnigenous stellarator, co-optimized with distributed
> phase-coherent RF actuation and realistic engineering constraints, provide measurable
> improvements in confinement or controllability relative to matched conventional
> stellarator baselines without worsening islands, transport, stability, structural burden,
> actuator complexity, or whole-system penalties?**

Release 0.1 does not have enough model authority to answer that full question. It provides a
reproducible lower-fidelity screen and the architecture required to escalate the question to
specialist solvers without changing the claim rules after seeing results.

## What is implemented now

### C6 geometry and magnetic screening

- versioned six-field-period C6 seed;
- matched five-field-period helical control;
- axisymmetric negative control;
- dimensionless 3-D toroidal boundary/axis representation;
- reduced field-strength spectrum;
- deterministic field-line integration and Poincaré output;
- rotational-transform screening output;
- resonant-overlap proxy.

### Omnigenity-oriented screening

- bounce-action variation proxy inspired by trapped-particle orbit physics;
- explicit distinction between the proxy and the second adiabatic invariant of a solved
  equilibrium;
- equal-budget deterministic seed optimization;
- multi-gate verdict logic rather than a single-objective success claim.

### Active phase-control research layer

- six-source phase-coherent actuator model;
- spatial-mode spectrum and target-mode purity;
- amplitude, phase, and geometry error injection;
- deterministic Monte Carlo;
- abstract feedback correction.

Under the committed error assumptions, median target spatial-mode purity increases from
approximately **99.21%** open loop to **99.93%** with abstract feedback. This is a
signal-processing result only; it is **not** evidence of RF/plasma coupling, heating, current
drive, or instability suppression.

### Magneto-structural and engineering screens

- magnetic-axis curvature and torsion;
- normalized support-burden proxy;
- blanket-space proxy;
- shielding-penetration burden proxy;
- plasma-facing heat-distribution proxy;
- cryogenic/control burden proxy;
- geometry/parameter-error Monte Carlo.

These outputs intentionally have **screening authority only**. They do not replace FEA,
materials qualification, neutronics, thermal-hydraulics, or cryogenic engineering.

### Evidence and falsification infrastructure

- A/B candidate/control protocol;
- ablations;
- negative controls;
- deterministic seeds;
- provenance hashes;
- machine-readable evidence bundle;
- explicit loss ledger;
- kill criteria;
- staged claim authority;
- release SHA-256 manifest;
- one authoritative GREEN/RED command.

## A useful negative result already exposed

The `no_axis_helical_shaping` ablation can improve the internal composite objective.

That is **not** evidence that the 3-D stellarator shape should be removed. It exposes an
important limitation in the reduced model: rotational transform is currently parameterized
rather than generated self-consistently from a solved coil/equilibrium field.

IX-Fusion retains that result instead of hiding it. It is one of the reasons the next gate
must use an actual equilibrium and coil solver.

## Model-authority ladder

```text
geometry hypothesis
        ↓
solved 3-D equilibrium + nested surfaces + transform
        ↓
magnetic candidate
        ↓
coil realization + error fields + particle orbits
        ↓
confinement candidate
        ↓
finite-pressure stability + turbulence + edge/divertor + RF full-wave
        ↓
plasma candidate
        ↓
blanket/neutronics + fuel cycle + complete plant energy ledger
        ↓
fusion-performance candidate
```

Release 0.1 remains at the first stage.

## Intended external solver path

The repository detects but does not bundle specialist solvers. Its evidence contracts are
designed for later integration of:

- **DESC** or equivalent for 3-D MHD equilibrium/optimization;
- **SIMSOPT** or equivalent for stellarator coil and field optimization;
- **VMEC-class** equilibrium as an independent cross-check;
- guiding-center / fast-particle tools;
- MHD stability analysis;
- gyrokinetic / validated transport analysis;
- RF full-wave / deposition tools;
- neutronics / blanket / fuel-cycle tools.

An unavailable or failed external solver must remain `UNKNOWN`; the internal model is not
allowed to impersonate a higher-authority result.

## Run it

Python 3.11 or later is required.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python check_green.py
```

Linux/macOS:

```bash
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python check_green.py
```

Expected final line for an intact release:

```text
IX-FUSION: GREEN
```

**GREEN means repository integrity and reduced-order evidence reproduce. It does not mean
fusion has been achieved.**

Full walkthrough: [`docs/08_BUILD_AND_VALIDATE.md`](docs/08_BUILD_AND_VALIDATE.md).

## Reproduce the research artifacts

```bash
python scripts/run_poc.py
python scripts/run_secondary_studies.py
python scripts/reproduce_release.py --verify
```

To intentionally refresh committed release artifacts and their hash manifest:

```bash
python scripts/generate_release.py
```

## Repository map

```text
IX-Fusion/
├── src/ix_fusion/              # reduced scientific/control/evidence models
├── configs/                    # candidate, control, optimization and system inputs
├── tests/                      # deterministic unit and scientific-regression tests
├── results/                    # generated POC, baselines, ablations, Monte Carlo, evidence
├── schemas/                    # candidate/evidence/external-solver contracts
├── provenance/                 # hashes of user-supplied conceptual source repositories
├── BOM/                        # software, conceptual-system and research evidence BOMs
├── docs/                       # claim boundary, validation path, safety, assumptions, roadmap
├── scripts/                    # reproduction, manifest and release commands
├── check_green.py              # authoritative local/CI quality gate
├── PROOF_OF_CONCEPT.md
├── VALIDATION_REPORT.md
├── LICENSE                     # IX-Fusion Research & Evaluation License
└── MANIFEST.sha256
```

## Recommended reviewer path

For a skeptical technical review:

1. [`docs/02_CLAIM_BOUNDARY.md`](docs/02_CLAIM_BOUNDARY.md)
2. [`PROOF_OF_CONCEPT.md`](PROOF_OF_CONCEPT.md)
3. [`results/poc/verdict.json`](results/poc/verdict.json)
4. [`src/ix_fusion/field.py`](src/ix_fusion/field.py)
5. [`src/ix_fusion/omnigenity.py`](src/ix_fusion/omnigenity.py)
6. [`src/ix_fusion/optimizer.py`](src/ix_fusion/optimizer.py)
7. [`results/ablations/c6_ablations.json`](results/ablations/c6_ablations.json)
8. [`docs/12_MODEL_LIMITATIONS.md`](docs/12_MODEL_LIMITATIONS.md)
9. [`results/evidence/loss_ledger.json`](results/evidence/loss_ledger.json)
10. run `python check_green.py`

## Safety and physical-build boundary

IX-Fusion is not a physical reactor construction package. The conceptual system BOM keeps
major engineering categories visible but intentionally does not contain operational reactor
specifications, tritium-handling procedures, radiation-producing experiment instructions,
high-voltage/RF build procedures, superconducting-magnet fabrication instructions, or
cryogenic plant construction procedures.

See [`docs/10_SAFETY_AND_SCOPE.md`](docs/10_SAFETY_AND_SCOPE.md) and
[`docs/21_PHYSICAL_BUILD_BOUNDARY.md`](docs/21_PHYSICAL_BUILD_BOUNDARY.md).

## License

IX-Fusion is **source-available for research/evaluation only** under the custom
**IX-Fusion Research & Evaluation License 1.0**. It is not Apache-2.0 and is not presented as
OSI open-source software. Production, operational, manufacturing, distribution, and
commercial use require separate written permission.

See [`LICENSE`](LICENSE).

## Technical basis and provenance

The validation path is informed by current stellarator work on direct omnigenity
optimization, equilibrium optimization, coil optimization, coil/support co-optimization,
HTS field shaping, and real-time plasma-control methods. References are separated from
IX-Fusion findings in [`docs/17_REFERENCES.md`](docs/17_REFERENCES.md).

Concepts translated from earlier project repositories are documented in
[`docs/16_SOURCE_REUSE_MAP.md`](docs/16_SOURCE_REUSE_MAP.md) and source-archive hashes are
recorded in [`provenance/ORIGIN_INPUTS.json`](provenance/ORIGIN_INPUTS.json). Prior-repository
claims are not inherited as IX-Fusion evidence.

---

**The standard for this repository is not whether C6 wins. It is whether the repository can
tell us, reproducibly and without moving the goalposts, when C6 loses.**
