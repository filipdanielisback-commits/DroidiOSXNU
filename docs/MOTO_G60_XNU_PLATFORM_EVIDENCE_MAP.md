# Moto G60 to XNU platform evidence map

**Status: static source correlation only. This document is not a hardware bill of materials, XNU port, driver implementation, build result, or boot-support claim.**

## Purpose and method

This map connects public evidence for the Motorola Moto G60 (XT2135-2, codename `hanoip`) to the relevant areas of the pinned XNU source tree. It distinguishes:

- **Exact-build source** — declarations in Motorola's kernel release matching the reported Android build `S2RIS32.32-20-9-9-2-3`.
- **Owner-reported** — configuration details supplied by the device owner.
- **Community clue** — Android device-tree or configuration material for the shared `hanoip` target; useful for leads, not definitive proof for this exact handset.
- **XNU source area** — where the corresponding kernel responsibility appears in the pinned XNU source. A source-area match is not evidence of a working driver.
- **Confidence** — confidence in the stated hardware/source observation, not confidence that XNU supports it.

The Motorola source release is [MMI-S2RIS32.32-20-9-9-2-3](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3). Motorola's [publication issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574) names the matching XT2135-2 firmware package. The matching release is the primary device-side source baseline used below.

The XNU comparison baseline is the project-pinned revision recorded in `kernel/xnu-source-pin.json`. Its source-tree map is documented in [XNU subsystem research map](XNU_SUBSYSTEM_RESEARCH_MAP.md). Apple's public README describes XNU as a hybrid Mach/BSD kernel with IOKit and ARM64 support; that generic architecture statement does not establish support for this phone.

## Evidence scale

| Label | Meaning |
| --- | --- |
| High | Directly declared by the exact-build Motorola source or confirmed by a matching official source record |
| Medium | Direct source clue, but shared configuration, ambiguous comment, or incomplete component identification limits the conclusion |
| Low | Indirect/community configuration clue or only partial platform evidence |
| Unknown | Available public evidence does not identify the item sufficiently |

## Platform evidence map

| Device area | Moto G60 evidence and source | Confidence | Relevant XNU research area | Current interpretation / unresolved questions |
| --- | --- | --- | --- | --- |
| Device identity / board | Exact-build `sdmmagpie-hanoip-evt1-overlay.dts`: `model = "hanoip"`, MSM ID 365, board ID `0x4C/A100`. DVT overlays describe B100/B200 variants. | High for source declarations; low for this handset's physical board ID | `pexpert/`, `pexpert/arm/`, platform configuration | The source has multiple board variants. The physical board revision/ID in the owner's unit is not independently established. |
| CPU architecture | Owner device profile and Motorola source context identify an ARM64 Qualcomm platform. | High | `osfmk/arm64/`, `osfmk/kern/` | Architecture overlap only. CPU feature requirements, exception-level assumptions, topology, and startup contract remain unmapped. |
| CPU topology / SMP | Qualcomm platform source contains CPU/platform declarations; no complete XNU-compatible topology contract is recorded. | Low | `osfmk/arm64/`, `osfmk/kern/` | Core count/topology, CPU start protocol, and inter-processor interrupt behavior need separate source analysis. |
| Interrupt controller | Platform device-tree declarations exist in the matching Motorola source tree. | Low | `osfmk/arm64/`, `osfmk/kern/`, `pexpert/arm/` | Exact controller mapping, interrupt routing, and XNU integration are not yet documented. |
| Timers / timebase | Timer and clock facilities are referenced in Qualcomm platform source. | Low | `osfmk/arm64/`, `osfmk/kern/` | Timer source, frequency assumptions, per-CPU timer model, and timekeeping contract remain unverified. |
| Physical memory / MMU | Memory and reserved-memory declarations occur in the platform DTS material. | Low | `osfmk/arm64/`, `osfmk/vm/`, `pexpert/` | A runtime physical map, reserved regions, MMU attributes, and handoff assumptions have not been established for XNU. |
| IOMMU / DMA | Qualcomm SMMU-related declarations occur in platform source. | Low | `osfmk/`, `iokit/Kernel/`, `libkern/` | DMA coherency, stream IDs, address translation, and device isolation contracts are not inventoried. |
| Storage | `sdmmagpie-hanoi-base.dts` and `sdmmagpie.dtsi` contain UFS controller/PHY references. | Medium | `iokit/IOKit/`, `iokit/Kernel/`, `bsd/` | Source indicates a UFS platform path, not an XNU UFS driver. Controller details, dependencies, and XNU storage integration remain absent. |
| Clocks / reset / power | Base DTS and related includes reference clocks, regulators, interconnect, PM6150 and PM6150L devices. | Medium | `pexpert/`, `iokit/IOKit/`, `iokit/Kernel/` | This is Linux platform description evidence. Sequencing, firmware interactions, and an XNU power model are not established. |
| Display | `hanoi-panel.dtsi` includes a Tianma ILI7807S 678 panel definition, 1080×2460 timing and 60/120 Hz modes. | Medium | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | The panel source is a useful lead; the full display controller/DSI pipeline and physical panel revision are not verified. No XNU display driver is recorded. |
| Touchscreen | Exact-build `sdmmagpie-hanoi-touchscreen.dtsi` declares SPI compatible `tchip,ilitek`. A separate community tree contains an NVT sysfs clue. | Medium for exact-build DTS declaration; low for fitted controller | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | Preserve the Ilitek/NVT discrepancy. The physical controller and revision remain unresolved; no XNU input driver is recorded. |
| USB / Type-C | Qualcomm USB and Type-C platform references occur in the Motorola source tree. | Low | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | Controller, PHY, port role behavior, power events, and XNU integration need further source mapping. |
| Wi-Fi | Community `hanoip` configuration refers to Qualcomm WLAN software components such as `qcwcn` / `qca_cld3`; module/directory naming includes QCA6390 clues. | Low | `bsd/net/`, `bsd/netinet/`, `iokit/IOKit/`, `libkern/` | Software-stack names do not prove the physical radio identity, bus wiring, firmware needs, or XNU support. |
| Bluetooth | Community Android configuration indicates Qualcomm Bluetooth integration, but does not conclusively identify the fitted controller and transport. | Low | `bsd/`, `iokit/IOKit/`, `libkern/` | Controller, transport, power sequencing, firmware, and XNU stack integration remain unknown. |
| Audio | `sdmmagpie-hanoi-audio-overlay.dtsi` references Qualcomm DSP/MI2S and Bolero-related nodes. | Medium | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | Audio path clues are present; exact codec population, routes, DSP contract, and XNU audio integration are not confirmed. |
| GPU | Community Android board configuration names Adreno 618. | Low | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | This is Android configuration evidence, not proof of the exact physical GPU revision or a public XNU graphics driver. |
| Cameras | `sdmmagpie-camera-sensor-mot-hanoip-evt1-overlay.dtsi` describes rear main, wide, depth, and front camera topology. A comment mentions S5KHM2/OV64B ambiguously. | Medium for topology; low for exact sensors | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | Treat sensor part numbers as unconfirmed. CSI/ISP, sensor control, clocks, power, and XNU capture support are not mapped. |
| NFC | `sdmmagpie-hanoip-common-overlay.dtsi` declares `qcom,nq-nci` on I2C at address `0x28`. | Medium | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | The NCI/I2C declaration is a useful source lead; exact module population and power dependencies remain to be confirmed. |
| Fingerprint | `sdmmagpie-hario-fps-overlay.dts` includes an `fpc,fpc1020`-compatible configuration. | Medium | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | This does not prove the fitted sensor or provide secure biometric services. |
| SAR / proximity-related sensing | `sdmmagpie-hanoip-sensor-overlay.dtsi` declares a Semtech SX933x device. | Medium | `iokit/IOKit/`, `iokit/Families/`, `libkern/` | Exact fitted variant and sensor role need confirmation; no XNU sensor service is recorded. |
| Thermal / battery / charging | Power-management and thermal-related platform references occur in the broader source material. | Low | `pexpert/`, `iokit/IOKit/`, `bsd/` | Exact fuel-gauge, charger, thermal-zone and policy details are not yet inventoried. |
| Platform handoff | No compatible XNU handoff contract is documented for this device. | Unknown | `libsa/`, `osfmk/arm64/`, `pexpert/` | Entry environment, platform description, memory ownership, and early initialization assumptions remain an overarching blocker. |

## Source pointers

### Motorola exact-build source

All links below point to the matching Motorola release tag:

- [Hanoip EVT1 overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-evt1-overlay.dts)
- [Hanoip common overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi)
- [Hanoip sensor overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-sensor-overlay.dtsi)
- [Hanoip EVT1 camera overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-camera-sensor-mot-hanoip-evt1-overlay.dtsi)
- [Hanoi panel definition](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/hanoi-panel.dtsi)
- [Hanoi touchscreen definition](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-touchscreen.dtsi)
- [Hanoi audio overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-audio-overlay.dtsi)
- [Hanoi base DTS](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-base.dts)
- [Motorola publication record for the matching firmware build](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)

### XNU research references

- [Pinned XNU source metadata](../kernel/xnu-source-pin.json)
- [XNU ARM64 source audit](XNU_ARM64_SOURCE_AUDIT.md)
- [XNU subsystem research map](XNU_SUBSYSTEM_RESEARCH_MAP.md)
- [Moto G60 XNU driver gap matrix](MOTO_G60_XNU_DRIVER_GAP_MATRIX.md)
- [Moto G60 exact-build kernel source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md)
- [Moto G60 wireless research](MOTO_G60_WIRELESS_RESEARCH.md)

## Highest-value unresolved questions

1. Which board ID/revision corresponds to the owner's physical XT2135-2?
2. Can the touchscreen controller discrepancy be resolved from authoritative exact-variant evidence?
3. What are the exact CPU topology, interrupt controller, timer/timebase, memory map, reserved regions, and IOMMU contracts?
4. What are the physical Wi-Fi/Bluetooth combo identity and host interfaces?
5. Which exact camera sensors, audio codec paths, fingerprint component, and NFC module are populated in this regional unit?
6. What platform handoff assumptions would have to be satisfied before XNU's ARM64 code could even be meaningfully evaluated on this board?

## Conclusion

The evidence is strongest for the exact-build source declarations and weaker for replaceable/population-dependent components and the physical board revision. The map provides a traceable research index; it does not convert Linux device-tree entries into XNU drivers. Every listed XNU area remains a research mapping, and no Moto G60 XNU platform implementation or hardware validation is claimed.

## Scope

Static source review and host-side documentation only. No handset access, firmware extraction, boot configuration changes, flashing, partition modification, or device storage changes are part of this milestone.
