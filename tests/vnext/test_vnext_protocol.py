from pathlib import Path

from ix_fusion.vnext import Authority, EvidenceRef, GATES, evaluate_gate, load_seed_league


ROOT = Path(__file__).resolve().parents[2]


def test_no_seed_is_privileged():
    seeds = load_seed_league(ROOT / "configs" / "vnext" / "seed_league.json")
    assert len(seeds) >= 4
    assert not any(seed.privileged for seed in seeds)


def test_low_authority_evidence_cannot_promote_equilibrium_gate():
    gate = next(g for g in GATES if g.gate_id == "G1_EQUILIBRIUM")
    evidence = [
        EvidenceRef(eid, Authority.REDUCED_MODEL, True, "toy")
        for eid in gate.required_evidence_ids
    ]
    verdict = evaluate_gate(gate, evidence)
    assert not verdict.passed
    assert set(verdict.insufficient_authority) == set(gate.required_evidence_ids)


def test_failed_evidence_blocks_gate():
    gate = next(g for g in GATES if g.gate_id == "G2_COILS")
    evidence = [
        EvidenceRef(eid, Authority.COIL_REALIZATION, eid != "coil_strain", "solver")
        for eid in gate.required_evidence_ids
    ]
    verdict = evaluate_gate(gate, evidence)
    assert not verdict.passed
    assert verdict.failed == ("coil_strain",)
