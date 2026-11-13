# DroidXNU XNU architecture alignment

**Status: completed static architecture review; no code or device implementation is claimed.**

## Purpose

DroidXNU intends to use Apple's public XNU kernel as its actual kernel foundation. HakiOS is a useful reference because its public documentation describes an XNU-on-Android research project with a common kernel repository, separate SoC/device layers, and a QEMU research target.

This review extracts architectural ideas only. It does not copy HakiOS source, claim compatibility with HakiOS, or provide device setup or boot instructions.

## HakiOS architecture observed

Based on the HakiOS repository README and its "How the repositories fit" documentation:

| Layer | HakiOS's documented organization | Relevance to DroidXNU |
|---|---|---|
| Common core | One common repository for the XNU port, common drivers, tools, documentation, and shared components | Keep shared XNU research separate from Moto G60-specific facts |
| SoC layer | SoC-family configuration and shared SoC driver area | Avoid mixing chipset-family assumptions with one board's details |
| Device layer | Per-device repository/configuration with device-specific status and drivers | Give the XT2135-2 its own evidence-backed platform profile |
| Manifest/revision tracking | Device/SoC sources can be pinned to explicit revisions | Record exact upstream revisions and provenance for every dependency |
| Host-independent research | HakiOS documents a QEMU target that runs without a phone's hardware or Apple's userspace | Consider host-only test categories separately from hardware compatibility |
| Userspace | Kernel and userspace are treated as separate layers | Keep XNU kernel research distinct from the proprietary iOS system boundary |

Sources:
- HakiOS repository: https://github.com/oosexgang/hakios-xnu-kernel
- HakiOS README: https://github.com/oosexgang/hakios-xnu-kernel/blob/main/README.md
- HakiOS repository architecture: https://github.com/oosexgang/hakios-xnu-kernel/blob/main/docs/porting/repositories.md
- HakiOS documentation index: https://github.com/oosexgang/hakios-xnu-kernel/blob/main/docs/index.md

The HakiOS README currently identifies XNU revision `xnu-8796.121.2` as its base and describes a POCO X5 Pro 5G device layer. Those are HakiOS project facts, not DroidXNU's source baseline or device facts.

## DroidXNU's current baseline

DroidXNU currently records:

- Upstream XNU: `apple-oss-distributions/xnu`
- Pinned tag: `xnu-12377.121.6`
- Pinned commit: `ac9718fb1af618d5ce8678d0dc6e8a58f252216f`
- Initial device research: Motorola Moto G60 XT2135-2 (`hanoip`)
- Evidence level: static source research and host-side tests only

See [XNU source baseline](XNU_SOURCE_BASELINE.md) and [Moto G60 feasibility](MOTO_G60_XNU_FEASIBILITY.md).

## Architectural decisions for DroidXNU

1. **XNU is the kernel foundation.** The project is not an Android application, launcher, theme, or iOS-style UI.
2. **Common and device-specific work must remain separate.** General XNU research must not be mixed with Moto G60 board assumptions.
3. **SoC facts and board facts must remain distinguishable.** A platform codename or marketed chipset label is not enough to establish identical hardware.
4. **The XNU pin is authoritative for this project's source baseline.** HakiOS's XNU revision is not silently substituted.
5. **HakiOS is an architecture reference, not a dependency.** No HakiOS code, patches, drivers, binaries, or device configs are copied by this review.
6. **QEMU is only a future host-side research possibility.** No DroidXNU QEMU target or successful XNU execution is claimed.
7. **The userspace boundary stays explicit.** A kernel port would not, by itself, recreate the complete iOS operating system.

## What this comparison does not establish

- It does not establish that the Moto G60 can run XNU.
- It does not establish that HakiOS supports the Moto G60 or that its POCO X5 Pro drivers are portable.
- It does not establish that the current DroidXNU XNU pin can be built for the target.
- It does not provide a compatible boot environment, device drivers, firmware, or iOS userspace.
- It does not authorize copying third-party code without a separate provenance and license review.

## Next research deliverables

- A proposed source-tree layout that separates common XNU research, SoC evidence, and per-device profiles.
- A static map of the pinned XNU source's ARM64/platform abstractions to the still-unresolved Moto G60 requirements.
- A source provenance and license checklist for any future external contribution.
- Additional synthetic host-side tests for metadata consistency.

All current work remains source review, documentation, and host-side testing. No device operations are part of this milestone.
