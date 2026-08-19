# IX-StellaratorForge — executable evidence overview

Release: **0.5.0**

## SFR-1

SFR-1 Rev A remains the steady-state reference architecture. Its v0.4 proof-of-concept and maximum in-repository computational closure artifacts are preserved unchanged:

- PoC verdict: `PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED`
- maximum closure verdict: `MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN`

The SFR-1 PoC verifies executable architecture validation, D-T burn arithmetic, confinement requirements, target-vs-screened power accounting, RF resonance, source-term accounting and held-out magnetic reconstruction. The v0.4 maximum closure layer adds production MHD seed generation, alternative vacuum magnet architecture screens, field-line tracing, geometry-only HTS strain proxies, TBR coverage constraints and conditional plant thresholds.

None of those artifacts impersonates DESC/VMEC++, kinetic transport, structural FEA, full 3-D OpenMC transport or hardware.

## SFR-2

v0.5.0 adds SFR-2 Rev A as a separate assumption-breaker, not as a promotion of SFR-1.

Its proof-of-concept claim is intentionally narrower:

> The 23/26/23/26 ABAB concept can be represented as a deterministic computational hypothesis with explicit geometry, compression assumptions, target-power matching, ISS04 sensitivity, promotion gates, and zero numerical credit for unmodeled phase/RF or flux-compression effects.

Primary SFR-2 verdict:

`NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY`

That negative result is retained. It prevents the repository from turning earlier exploratory percentages into evidence.

## Run

```bash
python scripts/run_sfr1_poc.py
python scripts/run_computational_closure.py
python scripts/generate_v040_evidence.py
python scripts/run_sfr2_screen.py
python check_stellarforge.py
```

Tracked SFR-2 outputs:

- `configs/reactor/sfr2_rev_a.json`
- `results/sfr2/sfr2_rev_a_screen_v050.json`
- `results/sfr2/SFR2_REVA_SCREEN_RESULT.md`
- `docs/reactor/12_SFR2_DYNAMIC_COMPRESSION.md`
- `docs/reactor/13_SFR2_PROMOTION_GATES.md`

## Promotion boundary

A low-authority model may reject a candidate. It may not declare one successful.

SFR-2 G1–G9 remain unrun until candidate-specific high-authority evidence exists. Actual fusion and net-electric operation remain outside software authority.
