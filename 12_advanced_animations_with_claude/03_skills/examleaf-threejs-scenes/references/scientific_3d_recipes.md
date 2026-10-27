# Scientific 3D recipes (fixture-fed)

Rule zero (report §9 accuracy invariant): any glyph that encodes science — a number, unit, label, arrow direction, lattice geometry, orbital shape or wave parameter — traces to a fixture field. Scene code receives fixtures as read-only props (`Object.freeze`), and QA diffs rendered text against fixtures. three.js renders; it never computes the science.

Ownership boundaries:
- Molecular structures and reactions: `examleaf-molecule-scenes` (RDKit-validated; optional 3Dmol.js view). Do not rebuild molecules in three.js.
- Equations and graphs: `examleaf-manim-scenes` / `examleaf-svg-scenes`.
- Hero spatial assets: `examleaf-blender-scenes`.
- This skill: orbitals, lattices, field lines, waves, trajectories and voxel recaps — light 3D (report §2.4, §4.5, §4.6).

## 1. Atomic orbitals (Chemistry / Physics)

Fixture (from `examleaf-science-chemistry` or `-physics`): orbital label (e.g. `2p_z`), a precomputed point cloud or isosurface mesh sampled from the validated wavefunction model, the probability threshold used, axis convention, and source claim IDs.

```text
fixture: { fixture_id, kind: "orbital", label, axis_up: "+z", threshold, points: [[x,y,z,phase],...] | mesh: {...},
           units: {x:"bohr", y:"bohr", z:"bohr"}, source_claim_ids, status }
```

Recipe: `THREE.Points` (or a mesh) built once; colour by phase sign from the fixture; slow orbit camera (§3 of the seek pattern); label tags from the fixture `label` via kinetic typography. Never sculpt "artistic" lobes or change lobe proportions for style.

## 2. Crystal lattices (Chemistry / Physics)

Fixture: lattice type, lattice constants with units, basis positions in fractional coordinates, number of unit cells to show, coordination numbers to state, source claims.

```text
fixture: { kind: "lattice", type: "fcc", a: 0.564, units: {a: "nm"}, basis: [[0,0,0],[0.5,0.5,0],...],
           cells: [3,3,3], species: [...], source_claim_ids, status }
```

Recipe: compute Cartesian positions once from fixture fields; `InstancedMesh` spheres per species; orthographic camera for counting tasks; unit-cell edges as `LineSegments`; seeded pop-in order for the reveal only (the positions never move randomly). Any count shown on screen ("12 nearest neighbours") is a fixture field.

## 3. Field lines (Physics)

Fixture: precomputed polylines integrated upstream from the validated source configuration (charges, currents, magnet model), with direction per line and sampling step, plus source claims.

Recipe: `Line` or tube geometry per polyline built once; draw-on by revealing a growing prefix of each polyline as a function of t (index = floor(u × n)); arrowheads placed at fixture-provided positions and directions. Never bend lines for aesthetics; never animate arrow directions except as the fixture defines.

## 4. Waves (Physics)

Fixture: amplitude, wavelength or wave number, frequency or angular frequency, phase, medium, units, and the **time scale** used for display (e.g. slowed 1:200) with the on-screen statement of that scale.

```text
y(x, t_phys) = A · sin(k·x − ω·t_phys + φ)       with A, k, ω, φ from the fixture
t_phys = (t − cue_at) × timeScale                  (timeScale from the fixture, stated on screen)
```

Recipe: plane geometry with vertices updated in `seek` from the formula (pure in t), or a shader with `uTime = t_phys`. Standing waves, superposition and interference use the same rule: every term from the fixture.

## 5. Trajectories and fixed-step physics replay (Physics, Rube-Goldberg-style demos)

[V5] shows a 3D "Rube Goldberg machine with natural-looking physics" (unverified Fable demo). ExamLeaf's version: the physics is computed upstream with a fixed-step integrator or an analytic solution, checked by the science skill, and stored as samples; the scene replays them.

- Validate: `python3 scripts/validate_trajectory_fixture.py fx.json --duration D --fps 30`.
- Replay: `sampleAt(fx, physT(t, cue_at, timeScale))` (seek pattern §2).
- Collisions, bounces and contacts are events in the fixture (`events: [{t, kind, body}]`), used to cue SFX via the cue sheet.
- A physics engine stepping in real time (or stepped per rendered frame inside `seek`) is forbidden: frames would depend on render order and worker count (#15, #17).

## 6. Planetary scale and orbits (Physics / editorial)

Fixture: radii, distances and periods with units, and the explicit scale compression used for display (e.g. sizes ×1, distances ÷1000). Show the compression on screen. Comparisons and orders of magnitude often fit `editorial-vox` better than 3D (style-guides matrix).

## 7. Voxel recaps and organelles (Biology / any)

- "Island of concepts" recap: decorative, seeded procedural layout allowed; labels are lesson terms from the approved script via the cue sheet.
- Cell organelles: compartment counts, relative placements and process states come from `examleaf-biology-scenes` state tables; voxels only render them.

## 8. Checklist per scientific 3D scene

- [ ] Every on-screen value and label maps to a fixture field (scene notes table).
- [ ] Fixture validated (status machine_checked or expert_approved; units; fixed step for trajectories).
- [ ] Display scalings (time scale, size compression) are fixture fields and are stated on screen.
- [ ] Camera does not move during a measurement or label reveal (#64).
- [ ] No randomness in scientific geometry; seeded randomness only in decoration.
- [ ] Double render identical on the render box (#17, #65).
