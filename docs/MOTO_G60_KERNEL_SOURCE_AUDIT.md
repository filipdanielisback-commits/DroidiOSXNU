# Moto G60 exact-build Linux kernel source audit

**Status: source-only research. No XNU driver has been implemented and no device boot is supported.**

## Target and exact source match

The project owner's device is:

- Motorola Moto G60, model XT2135-2
- 6 GB RAM
- 128 GB internal storage
- Software build: `S2RIS32.32-20-9-9-2-3`

Motorola's kernel-source issue #574 names the exact firmware package:

`XT2135-2_HANOIP_RETEU_12_S2RIS32.32-20-9-9-2-3_subsidy-DEFAULT_regulatory-XT2135-2-EUROPE_CFC.xml.zip`

Motorola marked the request as published and linked the source release:

- [Motorola kernel source release: MMI-S2RIS32.32-20-9-9-2-3](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)
- [Motorola source publication record, issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)

This is a substantially better source baseline than an unrelated kernel branch or a community ROM tree. It is a source match to the reported software build; it does not prove the phone's exact board revision or every replaceable component.

## Device-tree evidence inspected in the matching tag

The following files were read directly from the matching Motorola release tag.

| Area | Source evidence | Finding and limits |
| --- | --- | --- |
| Device identity | `sdmmagpie-hanoip-evt1-overlay.dts` | Sets `model = "hanoip"`, Qualcomm MSM ID 365, board ID 0x4C/A100 |
| Board variants | `sdmmagpie-hanoip-dvt1-overlay.dts`, `sdmmagpie-hanoip-dvt2-overlay.dts` | Same platform label but distinct board IDs B100 and B200. The owner's exact board ID has not been independently identified |
| Display | `hanoi-panel.dtsi` | Includes Tianma ILI7807S 678 1080×2460 video panel definition; DSI timing list includes 60 and 120 Hz |
| Touchscreen | `sdmmagpie-hanoi-touchscreen.dtsi` | Declares SPI device compatible with `tchip,ilitek`; exact retail part number/revision still needs confirmation |
| NFC | `sdmmagpie-hanoip-common-overlay.dtsi` | Declares `qcom,nq-nci` on QUP I2C at address 0x28 |
| SAR / proximity-related sensing | `sdmmagpie-hanoip-sensor-overlay.dtsi` | Declares Semtech SX933x on I2C; role and exact fitted part should be confirmed |
| Fingerprint | `sdmmagpie-hario-fps-overlay.dtsi` | Contains `fpc,fpc1020` and a generic Qualcomm fingerprint GPIO node; verify against this exact handset |
| Camera topology | `sdmmagpie-camera-sensor-mot-hanoip-evt1-overlay.dtsi` | Describes rear main, rear wide, rear depth and front camera connections. A source comment mentions S5KHM2/OV64B; do not treat that ambiguous comment as definitive sensor identification |
| Audio | `sdmmagpie-hanoi-audio-overlay.dtsi` | Enables Qualcomm audio/MI2S-related nodes and Bolero macro configuration; this is an audio integration map, not a confirmed codec bill of materials |
| Storage / power / buses | `sdmmagpie-hanoi-base.dts` and `sdmmagpie.dtsi` | References Qualcomm PM6150/PM6150L power-management devices, UFS, USB, clocks, regulators, interconnect and memory-controller infrastructure |

### Direct source links

- [Hanoip EVT1 overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-evt1-overlay.dts)
- [Hanoip common overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi)
- [Hanoip EVT1 camera overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-camera-sensor-mot-hanoip-evt1-overlay.dtsi)
- [Hanoi panel definition](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/hanoi-panel.dtsi)
- [Hanoi touchscreen definition](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-touchscreen.dtsi)
- [Hanoip sensor overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-sensor-overlay.dtsi)
- [Hanoi audio overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-audio-overlay.dtsi)
- [Fingerprint overlay](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hario-fps-overlay.dtsi)
- [Hanoi base device tree](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-base.dts)
- [SDM Magpie platform device tree](https://github.com/MotorolaMobilityLLC/kernel-msm/blob/MMI-S2RIS32.32-20-9-9-2-3/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi)

## Important correction: touchscreen identity conflict

The earlier community device-tree audit noted an `NVT-ts` sysfs path in a different Android tree. The exact-build Motorola kernel device tree instead declares an SPI touchscreen compatible with `tchip,ilitek`.

These are conflicting clues from different source trees. For now:

- Treat the exact-build Motorola DTS declaration (`tchip,ilitek`) as the stronger software-source lead.
- Do not state that the physical panel controller is conclusively identified.
- Resolve the conflict through additional exact-build driver/source references before writing an XNU touchscreen driver.

## Preliminary Linux-to-XNU gap matrix

| Subsystem | Linux-side evidence | XNU-side status | Priority |
| --- | --- | --- | --- |
| ARM64 CPU / boot | Qualcomm platform device tree and ARM64 kernel source | No platform bring-up code | Critical |
| Interrupts / timers / SMP | Platform DTS and SoC support code exist in Linux source | No XNU platform implementation | Critical |
| Memory map / MMU / IOMMU | Reserved memory and Qualcomm SMMU descriptions | No XNU mapping or IOMMU integration | Critical |
| Clocks / regulators / power | PM6150/PM6150L and clock/regulator descriptions | No XNU power framework integration | Critical |
| UFS storage | UFS controller and PHY references | No XNU storage driver | Critical |
| Display | Tianma ILI7807S panel and Qualcomm DSI/SDE references | No XNU display pipeline or panel driver | High |
| Touch | SPI `tchip,ilitek` node | No XNU SPI/touch driver | High |
| USB | Qualcomm USB and Type-C references | No XNU USB/Type-C integration | High |
| Audio | Qualcomm audio DSP, MI2S and Bolero references | No XNU audio path | Medium |
| WLAN / Bluetooth | Not conclusively identified in the DTS files reviewed so far | No XNU radio drivers | High |
| Cameras | Qualcomm camera framework and hanoip sensor topology | No XNU camera framework/driver | Medium |
| NFC | `qcom,nq-nci` I2C node | No XNU NFC driver | Low |
| Fingerprint | FPC1020 and generic fingerprint GPIO nodes | No XNU biometric integration | Low |
| Sensors | Semtech SX933x and sensor overlay references | No XNU sensor stack | Medium |

Priority is a planning estimate, not a claim that any component is easy to port.

## Licensing and source-handling notes

The device-tree files inspected contain GPL version 2 notices. The Motorola kernel release is Linux kernel source, not an XNU codebase. Before any reuse, review the complete applicable license notices and obligations. This project currently records findings and links only; it does not copy Motorola kernel code or proprietary vendor blobs into DroidiOSXNU.

Do not import firmware binaries, calibration data, keys, device dumps, or proprietary files. Keep this work as source analysis and documentation.

## Next research tasks

- [x] Find the Motorola source release matching the owner's exact software build.
- [x] Inspect the matching tag's hanoip board overlay and selected peripheral device-tree files.
- [x] Record the display panel and touchscreen software-interface clues from the exact tag.
- [ ] Determine which hanoip board ID corresponds to the owner's physical XT2135-2.
- [ ] Resolve the touchscreen NVT-versus-Ilitek source discrepancy.
- [ ] Inspect WLAN/Bluetooth and UFS driver bindings in the same release.
- [ ] Identify the platform's interrupt controller, timer, CPU topology, memory map and boot assumptions.
- [ ] Turn the gap matrix into a staged, host-side XNU feasibility plan.

## Scope and safety

This is static source research. Do not flash kernels, alter boot partitions, unlock or change boot settings, or attempt to boot XNU on the phone. The normal operating system should remain untouched.
