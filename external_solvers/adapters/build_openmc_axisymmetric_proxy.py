#!/usr/bin/env python3
"""Build and optionally run an axisymmetric SFR-1 OpenMC breeding proxy.

This is NOT the G7 final 3-D stellarator model.  It is an executable CSG torus benchmark
for nuclear-data/material sensitivity before ParaStell/DAGMC geometry exists.  A G7 pass
must use the solved 3-D geometry including ports, divertor, coils and penetrations.
"""
from __future__ import annotations
import argparse, importlib.util, json, math
from pathlib import Path


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--li-atom-fraction",type=float,default=0.157)
    ap.add_argument("--li6-enrichment",type=float,default=0.60)
    ap.add_argument("--particles",type=int,default=10000)
    ap.add_argument("--batches",type=int,default=20)
    ap.add_argument("--run",action="store_true")
    args=ap.parse_args()
    if importlib.util.find_spec("openmc") is None:
        raise SystemExit("OpenMC is not installed. No deterministic TBR surrogate will be labeled OpenMC.")
    import openmc  # type: ignore
    if not (0 < args.li_atom_fraction < 1 and 0 < args.li6_enrichment < 1): raise SystemExit("invalid lithium fractions")
    args.out.mkdir(parents=True,exist_ok=True)
    # SFR-1 Rev A radial build, cm.  Axisymmetric proxy deliberately ignores ports/3-D shaping.
    R=800.0; plasma=170.0; first_wall=5.0; blanket=55.0; shield=45.0; vessel=10.0
    r0=plasma; r1=r0+first_wall; r2=r1+blanket; r3=r2+shield; r4=r3+vessel
    surfaces=[openmc.ZTorus(a=R,b=r,c=r) for r in (r0,r1,r2,r3,r4)]
    surfaces[-1].boundary_type="vacuum"
    w=openmc.Material(name="tungsten_first_wall_proxy");w.add_element("W",1.0);w.set_density("g/cm3",19.25)
    breeder=openmc.Material(name="PbLi_breeder_proxy")
    xli=args.li_atom_fraction; breeder.add_nuclide("Li6",xli*args.li6_enrichment,percent_type="ao");breeder.add_nuclide("Li7",xli*(1-args.li6_enrichment),percent_type="ao");breeder.add_element("Pb",1-xli,percent_type="ao");breeder.set_density("g/cm3",9.4)
    steel=openmc.Material(name="iron_shield_proxy");steel.add_element("Fe",1.0);steel.set_density("g/cm3",7.8)
    vessel_mat=openmc.Material(name="iron_vessel_proxy");vessel_mat.add_element("Fe",1.0);vessel_mat.set_density("g/cm3",7.8)
    plasma_cell=openmc.Cell(name="plasma_void",region=-surfaces[0])
    fw_cell=openmc.Cell(name="first_wall",fill=w,region=+surfaces[0] & -surfaces[1])
    breeder_cell=openmc.Cell(name="breeder_blanket",fill=breeder,region=+surfaces[1] & -surfaces[2])
    shield_cell=openmc.Cell(name="shield",fill=steel,region=+surfaces[2] & -surfaces[3])
    vessel_cell=openmc.Cell(name="vessel",fill=vessel_mat,region=+surfaces[3] & -surfaces[4])
    geom=openmc.Geometry([plasma_cell,fw_cell,breeder_cell,shield_cell,vessel_cell])
    mats=openmc.Materials([w,breeder,steel,vessel_mat])
    settings=openmc.Settings();settings.run_mode="fixed source";settings.particles=args.particles;settings.batches=args.batches
    # Ring of isotropic 14.1-MeV point sources on the magnetic axis; equal weights.
    sources=[]
    for phi in [2*math.pi*k/48 for k in range(48)]:
        s=openmc.IndependentSource();s.space=openmc.stats.Point((R*math.cos(phi),R*math.sin(phi),0.0));s.angle=openmc.stats.Isotropic();s.energy=openmc.stats.Discrete([14.1e6],[1.0]);s.strength=1/48;sources.append(s)
    settings.source=sources
    tally=openmc.Tally(name="TBR_PROXY");tally.filters=[openmc.CellFilter(breeder_cell)];tally.scores=["(n,Xt)"]
    tallies=openmc.Tallies([tally])
    model=openmc.Model(geometry=geom,materials=mats,settings=settings,tallies=tallies)
    model.export_to_xml(directory=args.out)
    meta={"authority":"axisymmetric_OpenMC_CSG_proxy_not_G7_3D","li_atom_fraction":args.li_atom_fraction,"li6_enrichment":args.li6_enrichment,"radial_build_cm":[r0,r1,r2,r3,r4],"ports_and_3d_shaping_included":False}
    (args.out/"proxy_metadata.json").write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n")
    if args.run:
        sp=model.run(cwd=args.out)
        with openmc.StatePoint(sp) as statepoint:
            t=statepoint.get_tally(name="TBR_PROXY")
            result={"TBR_proxy_mean_per_source":float(t.mean.sum()),"TBR_proxy_std_dev":float((t.std_dev**2).sum()**0.5),**meta}
        (args.out/"tbr_proxy_result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        print(json.dumps(result,indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
