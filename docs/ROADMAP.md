# Research roadmap

All milestones are goals. None should be interpreted as completed until evidence is linked here.

## Milestone 0 — repository foundations

- [x] Establish project scope and initial documentation.
- [x] Add a firmware/build-artifact ignore policy.
- [ ] Decide the repository license after reviewing the planned components.
- [ ] Add issue templates and a test-report template.

## Milestone 1 — Moto G60 inventory

- [ ] Record exact model/region variant and product identifiers.
- [ ] Verify SoC, boot architecture, memory, display, touch controller, storage, Wi-Fi, Bluetooth, audio, cameras, and sensors from reliable sources.
- [ ] Map each component to available public documentation and open-source drivers.
- [ ] Record boot-chain constraints and supported development interfaces.
- [ ] Publish an evidence-based compatibility matrix.

## Milestone 2 — host-side research

- [ ] Pin a public XNU source revision and record its license.
- [ ] Document the required toolchain and supported build host.
- [ ] Create reproducible source-fetch and integrity-check scripts.
- [ ] Establish tests that run without a phone.
- [ ] Document known gaps between public XNU source and iOS userspace.

## Milestone 3 — platform feasibility

- [ ] Assess whether the selected XNU revision supports the relevant ARM64 platform assumptions.
- [ ] Document required platform abstractions and driver work.
- [ ] Evaluate a non-destructive test strategy before any device experiments.
- [ ] Publish a feasibility report with blockers and unknowns.

## Milestone 4 — feature research

Track each subsystem separately: display, touchscreen, storage, USB, Wi-Fi, Bluetooth, audio, GPU, sensors, cameras, and power management. A feature is not "working" until a reproducible test report is attached.

## Milestone 5 — future device assessments

After the Moto G60 inventory is complete, assess each device independently:

- Redmi Note 13 Pro 5G
- POCO X5 5G
- POCO X6 Pro 5G
- Google Pixel 4a
- Redmi Note 10 Pro

A shared SoC does not guarantee identical boot firmware, board wiring, display, touch, or peripheral support.
