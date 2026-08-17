# Software Build and Validation Walkthrough

This is the complete supported "build" walkthrough for release 0.1. It builds and validates
the **software research package**, not fusion hardware.

## Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python check_green.py
```

## Linux/macOS shell

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python check_green.py
```

## Reproduce the research outputs directly

```bash
python scripts/run_poc.py
python scripts/run_secondary_studies.py
python scripts/reproduce_release.py --verify
```

## Inspect optional specialist solvers

```bash
python -m ix_fusion solvers
```

The command only reports whether supported external tooling is present. Absence of an
external solver is not silently replaced by synthetic high-fidelity data.

## Meaning of GREEN

`IX-FUSION: GREEN` means the repository is internally consistent, tests pass, committed
reduced-order results reproduce, required evidence files are present, and release hashes
match. It does **not** mean fusion physics has been validated or a reactor is safe/buildable.
