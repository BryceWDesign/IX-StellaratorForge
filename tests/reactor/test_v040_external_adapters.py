from pathlib import Path
import ast

ROOT=Path(__file__).resolve().parents[2]

def test_external_adapters_are_real_executable_code_not_empty_templates():
    names={
        'run_desc_equilibrium.py','run_vmecpp_equilibrium.py',
        'build_openmc_axisymmetric_proxy.py','analyze_openmc_3d_tbr.py',
        'validate_production_receipt.py','validate_confinement_evidence.py',
    }
    for name in names:
        p=ROOT/'external_solvers/adapters'/name
        text=p.read_text()
        ast.parse(text)
        assert 'placeholder' not in text.lower()
        assert len(text)>500

def test_openmc_proxy_is_explicitly_not_final_3d_g7():
    text=(ROOT/'external_solvers/adapters/build_openmc_axisymmetric_proxy.py').read_text()
    assert 'NOT the G7 final 3-D stellarator model' in text
    assert '(n,Xt)' in text
    assert 'ZTorus' in text
