# Moto G60 hardware-to-XNU driver gap matrix

**Status: planning document based on public source review. This is not a port, compatibility claim, or device test result.**

## Purpose

This matrix translates the available Moto G60 Linux device-tree and Android configuration evidence into research questions for a hypothetical XNU platform. It separates:

1. what public source currently indicates about the phone;
2. what an XNU implementation would need at an architectural level;
3. what is still unknown or unimplemented.

Apple's public XNU source describes a hybrid Mach/BSD kernel, IOKit driver APIs, ARM64 support, and platform-specific code in `pexpert`. ARM64 support in XNU does **not** mean that an arbitrary ARM64 Android phone is supported. The SoC platform, boot environment, memory layout, interrupts, and drivers remain device-specific.

Reference: [Apple's public XNU source and README](https://github.com/apple-oss-distributions/xnu).

## Evidence labels

- **Exact-build source** — found in Motorola's kernel release matching the owner's reported build.
- **Community-tree clue** — found in a public `hanoip` Android tree; useful as a lead, not proof of this exact unit's hardware.
- **Owner-confirmed** — supplied by the device owner.
- **Unknown** — evidence is insufficient.
- **Not implemented** — no DroidiOSXNU implementation or test is recorded.

## Driver and platform gap matrix

| Subsystem | Current evidence | XNU-side requirement | DroidiOSXNU status | Priority / blocker |
| --- | --- | --- | --- | --- |
| CPU / ARM64 execution | Exact-build Motorola source targets an ARM64 Qualcomm platform | Compatible exception level, CPU feature assumptions, startup and per-CPU initialization | Not implemented | Critical; CPU topology and boot handoff are not fully documented |
| Boot handoff / platform identity | Motorola Android build and board overlays are known; exact physical board ID is not | A supported, documented entry environment and platform description understood by XNU | Not implemented | Critical; board ID and boot contract unknown |
| Interrupt controller | Qualcomm platform DTS exists | Interrupt-controller discovery, routing, priorities and interrupt handling integrated with XNU | Not implemented | Critical; exact controller mapping and XNU interface not audited |
| Timers / clock source | Qualcomm clock and timer-related platform data exists in source tree | Stable timebase, per-CPU timers and scheduler clock integration | Not implemented | Critical; timer source and frequency need source-level confirmation |
| SMP / CPU topology | ARM64 multi-core SoC platform | CPU discovery, startup, inter-processor interrupts and synchronization | Not implemented | Critical; exact CPU topology and startup mechanism not documented |
| Physical memory / MMU | Device-tree memory and reserved-memory descriptions | Kernel virtual/physical map, page tables, cache attributes and reserved regions | Not implemented | Critical; exact runtime map and boot reservations unknown |
| IOMMU / DMA | Qualcomm SMMU references in platform DTS | DMA mapping, IOMMU domains, coherency and device isolation | Not implemented | Critical; device-specific stream IDs and mappings not inventoried |
| Power / regulators / clocks | PM6150/PM6150L and regulator/clock descriptions in exact-build source | Safe initialization and runtime control of rails, clocks, resets and dependencies | Not implemented | Critical; sequencing and required firmware interactions unknown |
| UFS storage | UFS controller and PHY references in exact-build source | Controller, PHY, DMA, interrupts, power sequencing and block-storage integration | Not implemented | Critical; no XNU driver or verified storage contract |
| Display / DSI | Tianma ILI7807S 678 panel definition and Qualcomm display references | Display controller, DSI host, panel sequencing, modes and framebuffer/console path | Not implemented | High; physical panel revision and display pipeline details incomplete |
| Touchscreen | Exact-build DTS has SPI `tchip,ilitek` compatible; separate community tree has NVT clue | SPI controller plus verified touchscreen protocol, interrupts and input integration | Not implemented | High; NVT-versus-Ilitek discrepancy unresolved |
| USB / Type-C | Qualcomm USB and Type-C references | USB host/device controller, PHY, role switching, Type-C and power events | Not implemented | High; exact port configuration and role behavior need audit |
| Wi-Fi | Community tree references Qualcomm CLD3/WCNSS and mixed QCA module names | Verified radio identity, host bus, firmware protocol, calibration interface and network integration | Not implemented | High; physical chip identity unknown |
| Bluetooth | Community tree indicates Qualcomm Android Bluetooth integration | Verified controller, transport, power sequencing and Bluetooth stack integration | Not implemented | High; controller and bus wiring unknown |
| Audio | Exact-build source references Qualcomm DSP, MI2S and Bolero | Audio DSP communication, codec paths, clocks, routing and audio framework integration | Not implemented | Medium; codec population and routes not confirmed |
| GPU / acceleration | Adreno 618 reported in public Android configuration | GPU command submission, memory management, interrupts and graphics framework integration | Not implemented | High; exact GPU platform details and public driver path not established |
| Cameras | Exact-build DTS describes camera topology; sensor population is not fully certain | Camera sensor control, CSI/ISP, clocks, power and capture pipeline | Not implemented | Medium; sensor identities and ISP interface need confirmation |
| NFC | Exact-build DTS declares `qcom,nq-nci` on I2C | I2C controller, NCI transport and NFC framework integration | Not implemented | Low; exact module and power dependencies need confirmation |
| Fingerprint | Exact-build overlay includes FPC1020-compatible configuration | Sensor bus, reset/interrupt and secure biometric service integration | Not implemented | Low; fitted part and secure-service requirements unknown |
| Sensors / proximity | Exact-build overlay includes Semtech SX933x | I2C/SPI transport, interrupt handling, sensor semantics and userspace interface | Not implemented | Medium; exact role and sensor set need confirmation |
| Thermal / battery / charging | Platform power-management and thermal references exist | Thermal zones, battery/charger telemetry, throttling and safe power policy | Not implemented | High; full policy and fuel-gauge details not inventoried |

Priority is a sequencing estimate, not a statement that a subsystem is easy or feasible. A single missing critical platform dependency can prevent all later subsystems from being meaningfully tested.

## Dependency order for research

This is a source-analysis order, not a device bring-up procedure:

1. **Freeze the evidence baseline.** Keep the exact Motorola source tag, firmware build string, board-overlay references and unresolved variants recorded.
2. **Document the platform contract.** Identify CPU topology, interrupt controller, timer, memory map, reserved regions, IOMMU, clocks and reset dependencies from public source.
3. **Review XNU architecture boundaries.** Map the required platform services to public XNU areas such as ARM64 machine-dependent code, `pexpert`, Mach VM and IOKit. Do not assume Apple-specific platform code is portable.
4. **Assess storage and console prerequisites.** Determine what would be needed for a hypothetical isolated development environment without changing the phone.
5. **Only then assess peripherals.** Display, touch, USB, networking, audio, GPU, camera, NFC, fingerprint and sensors depend on the platform foundation.
6. **Record feasibility honestly.** Mark each item as documented, partially understood, unknown, blocked, or independently implemented. Do not label a feature working without a reproducible test report.

## Host-side validation plan

The next safe engineering work can be done without interacting with the handset:

- maintain source links and checksums for public source snapshots;
- parse and compare the relevant DTS declarations across board overlays;
- write small host-side scripts to extract node names, compatibles, addresses and dependencies from source text;
- add unit tests for those parsers using checked-in, non-proprietary text fixtures;
- review public XNU headers and source to map architectural interfaces;
- produce a dependency graph and an unresolved-question list.

No phone firmware, calibration data, private dumps, keys, proprietary vendor blobs or boot images belong in these tests.

## Explicit non-goals

This milestone does not provide instructions for flashing, unlocking, changing boot settings, replacing the operating system, or attempting to boot an experimental kernel. It does not claim that iOS can run on the Moto G60. The public XNU repository is a kernel source release, not the complete iOS operating system, and public ARM64 support alone is insufficient for device compatibility.

## Sources

- [Apple XNU source repository and architecture overview](https://github.com/apple-oss-distributions/xnu)
- [Motorola exact-build kernel release](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)
- [Motorola publication record for the matching XT2135-2 build](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)
- [DroidiOSXNU exact-build kernel source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md)
- [DroidiOSXNU WLAN/Bluetooth research audit](MOTO_G60_WIRELESS_RESEARCH.md)
- [DroidiOSXNU device-tree audit](MOTO_G60_DEVICE_TREE_AUDIT.md)

## Current conclusion

The Moto G60 has a useful public Linux source baseline for several peripherals, but the most important XNU platform dependencies remain unimplemented and partly undocumented. The project is still at the **hardware inventory and feasibility research** stage. A host-side source-analysis toolchain is the appropriate next milestone.
