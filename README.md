# DroidXNU

**Research into Apple's open-source XNU kernel as a foundation for an independent system on Android hardware.**

The initial hardware research target is the **Motorola Moto G60 (XT2135-2)**. DroidXNU is not an iOS clone or Android theme: the technical goal is to study XNU itself as the kernel foundation. The project is currently at static source research and host-side validation; no Moto G60 XNU port, target build, device driver, or bootable system has been demonstrated.

> **Status: early research. XNU is the intended kernel foundation, not an implemented device port.**

## Project direction

- Treat Apple's public XNU source as the kernel baseline and keep its exact upstream revision pinned.
- Fetch that exact revision into a separate ignored local source checkout; do not blur upstream Apple code with DroidXNU-owned changes.
- Separate common XNU research from SoC-specific and device-specific research.
- Document the platform abstractions and driver gaps that stand between generic ARM64 source support and a particular phone.
- Build host-side validators, parsers, and tests before considering any platform implementation.
- Keep the distinction between XNU and the proprietary parts of iOS explicit.

## Architecture reference

The HakiOS project is a useful public reference for the *organization* of an XNU-on-Android research project. Its documentation separates a common kernel and tools layer from SoC and per-device layers, and it describes QEMU as a separate hardware-independent research target. DroidXNU records that architecture as a design reference only; it does not assume HakiOS code, drivers, or device support can be reused on the Moto G60.

See [DroidXNU architecture alignment](docs/XNU_ARCHITECTURE_ALIGNMENT.md), the [XNU subsystem research map](docs/XNU_SUBSYSTEM_RESEARCH_MAP.md), the [Moto G60 XNU platform evidence map](docs/MOTO_G60_XNU_PLATFORM_EVIDENCE_MAP.md), and the new [XNU ARM64 platform foundations](docs/XNU_ARM64_PLATFORM_FOUNDATIONS.md).

## Initial device

| Device | Platform identifier | Status |
| --- | --- | --- |
| Motorola Moto G60 XT2135-2 | `hanoip`; exact board revision unresolved | Static research target only |

Device support is not implied by appearing in this table. The Moto G60 needs its own verified platform description, source review, and independently evidenced implementation.

## Project layout

- `docs/` — architecture, research notes, roadmap, and legal boundaries.
- `devices/` — per-device research and configuration notes.
- `kernel/` — pinned XNU source metadata, source-fetch tooling, and kernel research notes.
- `boot/` — non-operational boot-flow research and host-only simulation.
- `drivers/` — hardware-driver research and implementation status.
- `tools/` — auditable host-side development utilities.
- `ipsw/` — documentation for inspecting firmware metadata; no proprietary files are stored.
- `tests/` — host-side checks and synthetic tests.
- `gui/` — optional research visualizations; not a kernel, bootloader, or installer.

## Technical reality

XNU is an open-source kernel, not the complete iOS operating system. Public XNU source does not include all proprietary iOS frameworks, services, platform components, firmware, or signing materials. ARM64 support in upstream XNU does not establish support for the Moto G60's specific SoC, board, memory map, interrupts, storage, or peripherals.

The current pinned baseline is documented in [XNU source baseline](docs/XNU_SOURCE_BASELINE.md). The current static assessment finds architecture-level ARM64 overlap only; Moto G60 compatibility is unproven. See [Moto G60 XNU feasibility](docs/MOTO_G60_XNU_FEASIBILITY.md), [XNU versus iOS system boundary](docs/XNU_VS_IOS_SYSTEM_BOUNDARY.md), and the [platform evidence map](docs/MOTO_G60_XNU_PLATFORM_EVIDENCE_MAP.md).

## Project boundaries

- Keep work to source research, documentation, host-side tools, and tests.
- The Apple XNU checkout is local and ignored; it is not committed into this repository.
- Do not commit IPSW files, extracted proprietary firmware, keys, certificates, personal data, or device dumps.
- Do not claim that a mockup or simulator is a real bootloader or device test.
- Review the exact license and notices for every external component before considering reuse.
- A repository-wide license has not yet been selected. Third-party components retain their own licenses.

See [Legal and firmware policy](docs/LEGAL.md), [Contributing](CONTRIBUTING.md), and [Roadmap](docs/ROADMAP.md).

DroidXNU is an independent research project and is not affiliated with or endorsed by Apple, Motorola, Qualcomm, or the HakiOS developers.
