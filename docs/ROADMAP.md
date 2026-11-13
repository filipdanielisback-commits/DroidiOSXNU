# DroidXNU research roadmap

All milestones are goals. A milestone is complete only when its evidence is linked here. Documentation or host-side tests must never be presented as proof of phone compatibility.

## Milestone 0 — repository foundations

- [x] Establish project scope and initial documentation.
- [x] Add a firmware/build-artifact ignore policy.
- [ ] Decide the repository license after reviewing planned components.
- [ ] Add issue templates and a test-report template.

## Milestone 1 — Moto G60 inventory

- [x] Record exact model/region variant and owner-supplied device configuration.
- [x] Locate the Motorola kernel source release matching the reported software build.
- [x] Review the matching source's major device-tree peripheral declarations.
- [x] Publish preliminary WLAN/Bluetooth software-stack clues while keeping physical chip identity unresolved.
- [x] Publish the initial hardware-to-XNU driver gap matrix.
- [ ] Verify remaining SoC, memory, interrupt, timer, storage, radio, audio, GPU, camera, and sensor details from authoritative sources.
- [ ] Resolve board-ID and touchscreen-controller discrepancies.
- [ ] Map components to public documentation and open-source driver references.

## Milestone 2 — host-side research

- [x] Pin a public XNU source revision and record its license.
- [x] Record upstream toolchain/build-host notes without claiming a validated DroidXNU build environment.
- [x] Add a host-only verifier for the pinned XNU tag object and peeled commit.
- [x] Document the boundary between public XNU and a complete iOS system.
- [x] Add a best-effort DTS/DTSI inventory parser and synthetic unit tests.
- [x] Add an explicitly non-operational host-side boot-flow simulator with synthetic tests.
- [x] Add a host-only JSON platform-profile validator and synthetic tests.
- [x] Publish a structured static platform dependency inventory with evidence, confidence, priority, and unresolved questions.
- [x] Add a browser-based research visualization with static tests; it is not a bootloader or installer.

## Milestone 3 — platform feasibility

- [x] Complete a static assessment of the selected XNU revision's documented ARM64 assumptions against the Moto G60 profile.
- [x] Document required platform abstractions and major driver gaps.
- [x] Publish the static feasibility report.
- [x] Publish a source-linked Moto G60-to-XNU platform evidence map.
- [ ] Resolve remaining hardware evidence gaps and board/component discrepancies.

See [Moto G60 XNU platform evidence map](MOTO_G60_XNU_PLATFORM_EVIDENCE_MAP.md) for the subsystem-by-subsystem source correlation and confidence labels.

## Milestone 4 — XNU architecture alignment

- [x] Review HakiOS's public high-level architecture and repository separation.
- [x] Record the common-kernel / SoC / device / host-test separation as a reference model.
- [x] State explicitly that HakiOS code and device support are not assumed reusable on the Moto G60.
- [x] Design a DroidXNU source-tree organization for common, SoC, and device research without importing third-party code.
- [ ] Document a provenance and license review checklist for any future external source consideration.

See [XNU ARM64 source architecture audit](XNU_ARM64_SOURCE_AUDIT.md) for the pinned source-tree responsibility map and current compatibility boundaries.

See [XNU architecture alignment](XNU_ARCHITECTURE_ALIGNMENT.md).

## Milestone 5 — feature research

- [x] Map Mach, BSD, IOKit, ARM64, and platform-specific source areas in the pinned XNU tree.
- [x] Record how the source areas relate to Moto G60 research without claiming target support.

See [XNU subsystem research map](XNU_SUBSYSTEM_RESEARCH_MAP.md).

Track display, touchscreen, storage, USB, Wi-Fi, Bluetooth, audio, GPU, sensors, cameras, and power management separately. A feature is not "working" until there is a clearly scoped, reproducible test report. Static source references alone are not implementation evidence.

## Milestone 6 — future platform assessments

Only after the initial Moto G60 research is well documented should additional devices be assessed independently. A shared SoC does not guarantee identical board wiring, firmware, display, touch, or peripheral support.
