# Moto G60 / XNU platform feasibility assessment

**Assessment type: static source review only. Outcome: not currently demonstrated feasible as a working device port.**

This report compares the pinned public XNU source baseline with the available Moto G60 research profile and Motorola exact-build Linux source findings. It is a documentary assessment, not a build, hardware test, boot test, or implementation plan for modifying a phone.

## Executive finding

There is one useful point of alignment: both the Moto G60 platform and the selected XNU source include ARM64 in their documented architecture context.

That alignment is necessary but far from sufficient. The public XNU README's ARM64 support does not establish support for the Moto G60's Qualcomm platform, board revision, firmware handoff, memory layout, interrupt controller, timers, storage controller, or peripherals. The inspected XNU source baseline documents Apple-oriented platform/build assumptions; no matching Moto G60 platform implementation has been identified.

**Current verdict: architecture-level overlap is confirmed; device-level compatibility is unproven, with critical platform gaps and unknowns.** There is not enough evidence to claim that this XNU revision can build for, initialize, or run on the XT2135-2.

## Evidence baseline

| Item | Current evidence | Confidence / limitation |
|---|---|---|
| Device | Motorola Moto G60, XT2135-2 | Owner-reported and correlated with Motorola's matching source publication |
| Android build | `S2RIS32.32-20-9-9-2-3` | Owner-reported; exact Motorola kernel release located |
| Motorola kernel source | `MMI-S2RIS32.32-20-9-9-2-3` | Exact-build source baseline |
| Platform identifiers | SDM Magpie / SM6150 references in source | Source-derived naming; do not infer unsupported chipset equivalences |
| Device codename | `hanoip` | Source-correlated; shared platform label does not identify every board variant |
| Device architecture | ARM64 | Device/source profile evidence |
| XNU baseline | `xnu-12377.121.6`, commit `ac9718fb1af618d5ce8678d0dc6e8a58f252216f` | Pinned public upstream revision; annotated tag is unsigned |
| XNU architecture | Upstream README lists ARM64 | Establishes source architecture support, not Moto G60 platform support |
| Physical board revision / board ID | Unresolved | No confirmed mapping to the owner's physical handset |
| Touchscreen controller revision | Conflicting source clues | Exact-build DTS says `tchip,ilitek`; another community tree contains an NVT clue |
| Wireless combo identity | Unresolved | Community driver names are clues, not confirmation of the fitted radio |

References: [XNU source baseline](XNU_SOURCE_BASELINE.md), [Moto G60 platform profile](../devices/moto-g60/platform-profile.json), [Motorola exact-build kernel audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md), and [hardware-to-XNU driver gap matrix](MOTO_G60_XNU_DRIVER_GAP_MATRIX.md).

## Feasibility matrix

Status labels mean:
- **Documented overlap** — relevant public source or architecture evidence exists, but this is not a compatibility test.
- **Partially documented** — some source references exist; important details remain unresolved.
- **Unknown / unverified** — the required platform contract has not been established.
- **Not implemented** — no DroidXNU implementation or test evidence exists.

| Area | Evidence and comparison | Status | Why it matters |
|---|---|---|---|
| CPU architecture | Moto G60 profile is ARM64; pinned XNU README lists ARM64 | Documented overlap | Architecture compatibility is only the starting point |
| CPU features and exception levels | Exact target CPU feature requirements and expected entry state have not been mapped against XNU | Unknown / unverified | Kernel assumptions must match the processor and execution environment |
| CPU topology and SMP | Qualcomm source contains platform data, but no complete XNU CPU discovery/startup/interrupt mapping is documented | Partially documented; not implemented | Multiprocessor operation depends on platform-specific coordination |
| Interrupt controller | Linux device-tree source provides platform declarations; equivalent XNU platform integration is absent | Partially documented; not implemented | Interrupt delivery is foundational for scheduling and device operation |
| Timers and clock source | Clock/timer references exist in Motorola source; XNU-compatible timebase and timer integration are not established | Partially documented; not implemented | Timekeeping and scheduling depend on reliable timer support |
| Physical memory and MMU | Device-tree memory and reserved-region information exists, but a validated XNU physical/virtual map is absent | Partially documented; not implemented | Memory management must match the actual platform contract |
| IOMMU and DMA | Qualcomm SMMU references appear in platform source; XNU mappings, domains and coherency behavior are not documented | Partially documented; not implemented | Device DMA cannot be assumed safe or compatible |
| Clocks, resets and regulators | PM6150/PM6150L and clock/regulator descriptions are present in Motorola source | Partially documented; not implemented | Platform components have interdependent power and clock requirements |
| Storage | UFS controller/PHY references exist; no XNU UFS integration or verified platform contract is recorded | Partially documented; not implemented | Storage is a major platform dependency |
| Display and touch | Panel and touchscreen software-interface clues exist; XNU display/touch support is absent | Partially documented; not implemented | Display pipeline and physical controller details remain incomplete |
| USB and Type-C | Qualcomm USB/Type-C source references exist; no XNU integration is recorded | Partially documented; not implemented | Controller, PHY and role behavior are platform-specific |
| Wi-Fi and Bluetooth | Community-tree clues only; physical radio identity unresolved | Unknown / not implemented | Driver choice and firmware interface cannot be selected confidently |
| Audio, GPU, cameras and sensors | Linux source contains subsystem clues, but no matching XNU drivers/framework integration is present | Partially documented; not implemented | Each subsystem requires its own hardware and software contract |
| Boot environment | Public XNU baseline describes Apple-oriented development/platform context; Moto G60 handoff contract is not established | Unknown / unverified | No claim can be made about a compatible entry environment |
| Build environment | Upstream README documents Apple/macOS-oriented prerequisites; no supported DroidXNU cross-build environment is validated | Unknown / unverified | No successful target build has been demonstrated |

## Required platform abstractions

At a high level, a platform-specific XNU implementation would need documented equivalents or integrations for:

1. **Machine-dependent CPU support:** CPU identification, feature assumptions, exception handling, per-CPU state and multiprocessor abstractions.
2. **Platform expert configuration:** board/platform identity, early platform services and hardware resource descriptions.
3. **Interrupt and time services:** interrupt-controller integration, timer source and clock/timebase interfaces.
4. **Memory management:** physical memory description, reserved regions, MMU attributes and DMA/IOMMU behavior.
5. **Power and interconnect services:** clocks, reset controls, regulators and dependencies between platform devices.
6. **Device frameworks and drivers:** storage, USB, display, input, radios, audio, graphics and sensors.
7. **System-level services outside the kernel:** a compatible userspace and supporting services would still be needed; see [XNU versus iOS system boundary](XNU_VS_IOS_SYSTEM_BOUNDARY.md).

This is a conceptual inventory of missing engineering areas, not a sequence of device operations.

## Main blockers

### Critical blockers

- No verified XNU platform support for the Moto G60's Qualcomm board.
- No established CPU startup, interrupt-controller, timer, or SMP integration.
- No validated physical memory map, reserved-memory contract, or IOMMU/DMA model.
- No documented compatible platform handoff contract.
- No demonstrated target build or host toolchain configuration for this project.

### Important unresolved hardware questions

- Which board revision and board ID correspond to the owner's physical XT2135-2?
- Which touchscreen controller revision is fitted?
- What exact wireless combo chip and bus interface are present?
- Which camera sensors, audio codec paths and peripheral revisions are populated on this unit?

These remain research questions. The project should not infer physical hardware from a shared codename or a community device tree.

## Recommended project direction

Continue with source-only work:

- Keep the pinned XNU and exact-build Motorola source references stable.
- Improve host-side parsers and tests using synthetic or appropriately licensed public text fixtures.
- Compare static device-tree declarations and record confidence/provenance for each finding.
- Map public XNU architectural interfaces to the required platform abstractions at a documentation level.
- Keep unresolved physical hardware identities explicit.
- Treat any future feasibility change as requiring new authoritative source evidence and separately reviewed safety and legal scope.

No phone access, bootloader interaction, firmware extraction, partition changes, flashing, or boot attempts are part of this assessment.

## Conclusion

The current evidence supports **ARM64 architecture overlap only**. It does not support a claim that XNU is compatible with the Moto G60, that the selected revision can be built for it, or that any device subsystem works under XNU.

The project remains at static inventory and feasibility research. The immediate engineering blocker is the absence of a documented XNU platform contract for this Qualcomm-based board, compounded by incomplete hardware identification and a lack of XNU driver implementations.

## Sources

- [Pinned public XNU source baseline](XNU_SOURCE_BASELINE.md)
- [Apple XNU repository](https://github.com/apple-oss-distributions/xnu)
- [Motorola exact-build kernel source release](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)
- [Motorola source publication record for XT2135-2](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)
- [Moto G60 exact-build kernel source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md)
- [Moto G60 hardware-to-XNU driver gap matrix](MOTO_G60_XNU_DRIVER_GAP_MATRIX.md)
- [Moto G60 platform profile](../devices/moto-g60/platform-profile.json)
