# Research roadmap

All milestones are goals. None should be interpreted as completed until evidence is linked here.

## Milestone 0 — repository foundations

- [x] Establish project scope and initial documentation.
- [x] Add a firmware/build-artifact ignore policy.
- [ ] Decide the repository license after reviewing the planned components.
- [ ] Add issue templates and a test-report template.

## Milestone 1 — Moto G60 inventory

- [x] Record exact model/region variant and owner-supplied device configuration.
- [x] Locate the Motorola kernel source release matching the reported software build.
- [x] Review the matching source's major device-tree peripheral declarations.
- [x] Publish preliminary WLAN/Bluetooth software-stack clues while keeping physical chip identity unresolved.
- [x] Publish an initial hardware-to-XNU driver gap matrix: [Moto G60 XNU driver gap matrix](MOTO_G60_XNU_DRIVER_GAP_MATRIX.md).
- [ ] Verify remaining SoC, boot architecture, memory map, interrupt, timer, storage, Wi-Fi, Bluetooth, audio, GPU, camera, and sensor details from authoritative sources.
- [ ] Resolve the board-ID and touchscreen-controller discrepancies.
- [ ] Map each component to available public documentation and open-source drivers.
- [ ] Record boot-chain constraints and supported development interfaces.

## Milestone 2 — host-side research

- [ ] Pin a public XNU source revision and record its license.
- [ ] Document the required toolchain and supported build host.
- [ ] Create reproducible source-fetch and integrity-check scripts.
- [ ] Establish tests that run without a phone.
- [ ] Document known gaps between public XNU source and iOS userspace.
- [x] Add a best-effort host-side DTS/DTSI inventory parser and synthetic unit tests; semantic parsing and real-source validation remain future work.
- [x] Add an explicitly non-operational host-side boot-flow simulator with synthetic tests: [simulator design](BOOT_FLOW_SIMULATOR.md).
- [x] Add a host-only JSON platform-profile validator and synthetic tests for the Moto G60 research profile.

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
