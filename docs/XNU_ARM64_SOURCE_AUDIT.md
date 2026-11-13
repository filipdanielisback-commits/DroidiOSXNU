# XNU ARM64 source architecture audit

**Status:** static source review only  
**Pinned baseline:** `xnu-12377.121.6`  
**Target research profile:** Motorola Moto G60 (XT2135-2), platform codename `hanoip`

This report maps the public XNU source tree to the kinds of platform responsibilities DroidXNU must understand. It is not a porting guide, build recipe, boot procedure, or claim of device compatibility.

## 1. What the pinned source establishes

The pinned upstream README describes XNU as a hybrid kernel combining Mach, FreeBSD-derived components, and IOKit. It explicitly lists `x86_64` and `ARM64` as supported processor architectures.

That is an architecture-level statement. It does not establish support for a Qualcomm SoC, the Moto G60 board, its memory map, interrupt topology, timers, storage, display, radios, or other peripherals. A generic ARM64 implementation is not a device platform implementation.

Primary references:

- [Pinned XNU source tree](https://github.com/apple-oss-distributions/xnu/tree/xnu-12377.121.6)
- [Pinned XNU README](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/README.md)
- [Pinned source metadata](../kernel/xnu-source-pin.json)

## 2. Source-tree responsibility map

The following descriptions are taken from the pinned upstream README and source-tree organization. They describe upstream XNU responsibilities, not completed DroidXNU components.

| Upstream area | Responsibility described by upstream | DroidXNU research relevance |
|---|---|---|
| `osfmk/` | Mach-based kernel subsystems | Understand core kernel abstractions separately from phone-specific integration. |
| `osfmk/arm64/` | ARM64-specific kernel implementation is present in the tree | Audit architecture code as generic ARM64 support; do not infer support for the target SoC. |
| `bsd/` | BSD subsystems | Document the kernel's BSD-facing services and their dependencies without assuming a complete iOS userspace. |
| `libkern/` | C++ IOKit library code for drivers and kernel extensions | Study driver-framework concepts and interfaces; no Moto G60 driver is implemented here by this project. |
| `pexpert/` | Platform-specific code, including interrupt handling and atomics | A key boundary between generic kernel code and platform-specific facts. |
| `libsa/` | Kernel bootstrap code | Record as an upstream source area only; no target startup or boot implementation is in scope. |
| `config/` | Exported API configurations for supported architectures and platforms | Track configuration provenance and avoid inventing a target configuration. |
| `security/` | Mandatory Access Check policy interfaces and related implementation | Understand kernel security interfaces as part of the common-kernel review. |
| `libsyscall/` | System-call library interface for userspace programs | Helps document the kernel/userspace boundary; it is not the full iOS userspace. |
| `tools/`, `tests/` | Utilities for testing, debugging, profiling, and tests | Useful reference areas for host-side research and test design. |

## 3. ARM64 is necessary, not sufficient

A phone platform needs more than an instruction-set implementation. The target-specific evidence map must separately address:

- CPU and multiprocessor topology;
- exception and interrupt-controller integration;
- architectural and platform timer behavior;
- physical memory layout and memory attributes;
- address translation and DMA/IOMMU relationships;
- bus discovery and device descriptions;
- clocks, resets, regulators, and power domains;
- storage and console/debug facilities;
- display, touch, audio, wireless, camera, and sensor devices.

This list is a research taxonomy, not an implementation checklist or instructions for modifying a device.

## 4. Moto G60 evidence status

The repository already contains a device profile, source audits, and a driver-gap matrix. Those materials are static evidence collected from public source and owner-supplied model/build details. They do not demonstrate that the corresponding hardware is supported by XNU.

| Topic | Current project status | What can safely be concluded |
|---|---|---|
| CPU architecture | ARM64 is the relevant XNU architecture family | Generic source architecture overlap only. |
| SoC / platform | Motorola source references the `hanoip` platform family and Qualcomm-specific platform components | Exact compatibility with XNU platform code is unproven. |
| Board revision | Exact physical board revision remains unknown | Do not select a board configuration based on a family codename alone. |
| Memory / interrupts / timers | Public device-source clues exist, but no XNU platform implementation is established | Requires careful source-level evidence mapping. |
| Storage / USB | Vendor-source references are recorded in the device research | No XNU controller or platform support is implemented. |
| Display / touch | Panel and touchscreen source clues are recorded; controller identity is not fully resolved | No XNU display or touch driver is implemented. |
| Wi-Fi / Bluetooth | Android-side software-stack clues are documented; physical radio identity remains unresolved | No XNU wireless support is implemented. |
| Audio / camera / sensors / GPU | Research notes and unresolved details exist | No XNU drivers or working subsystem support are implemented. |

See [Moto G60 research sources](MOTO_G60_RESEARCH_SOURCES.md), [device-tree audit](MOTO_G60_DEVICE_TREE_AUDIT.md), [kernel-source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md), and [driver-gap matrix](MOTO_G60_XNU_DRIVER_GAP_MATRIX.md).

## 5. DroidXNU source organization decision

For research notes and future host-side metadata, retain these boundaries:

- `kernel/`: upstream revision metadata and common XNU source research;
- `devices/moto-g60/`: facts and evidence specific to XT2135-2;
- `docs/`: architecture, compatibility limits, provenance, and feasibility reports;
- `tools/`: host-only validators and parsers;
- `tests/`: synthetic tests that do not require phone access.

Do not place unverified Moto G60 assumptions in common-kernel notes. Do not copy third-party implementation code into the repository without a separate provenance and license review.

## 6. Build-environment finding

The pinned upstream README describes an Apple-oriented external build environment, including Xcode, SDK/KDK alignment for relevant Apple platforms, and additional dependencies. Its documented platform examples are not a validated build environment for DroidXNU or the Moto G60.

No DroidXNU kernel build has been performed. No target build configuration has been validated. This project does not provide device installation, boot, firmware, or boot-configuration procedures.

## 7. Next research deliverables

1. Extend the platform evidence map so each hardware statement has a source URL, source revision, confidence, and unresolved question.
2. Keep SoC-family claims separate from exact XT2135-2 board claims.
3. Review external code provenance and license terms before considering reuse.
4. Add host-side checks for the consistency of the source/evidence metadata.

## 8. Explicit non-claims

This audit does not claim that:

- XNU has been built for the Moto G60;
- the Moto G60 is supported by upstream XNU;
- a DroidXNU kernel, driver, bootloader, or bootable system exists;
- HakiOS code or device support can be reused on this target;
- public XNU source is the complete source for iOS.

DroidXNU remains an XNU-first research project, not an iOS-themed Android app or a demonstrated iOS port.
