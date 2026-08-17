# Kill Criteria

IX-Fusion components are hypotheses, not protected features.

## Kill the C6 seed if

- equal-authority high-fidelity optimization consistently converges to worse confinement or
  engineering results than matched controls;
- the C6 seed produces unacceptable islands/chaos or fast-particle losses that cannot be
  removed without erasing the seed;
- any observed advantage disappears under reasonable perturbations or independent reruns;
- the optimizer reliably removes C6 structure and the non-C6 solution is superior.

## Kill C3/C9 correction branches if

They do not improve a predeclared metric without unacceptable tail, complexity, or
robustness penalties. Release-0.1 ablations do not justify retaining either correction as a
core feature.

## Kill the active phased-RF branch if

Full-wave/deposition modeling or experiment shows no useful controllability advantage, or if
the actuator complexity/recirculating power exceeds the benefit.

## Kill an engineering layer if

It adds complexity without improving an independently measurable failure mode.

No kill criterion may be weakened after seeing an unfavorable result without a versioned,
explicit protocol change.
