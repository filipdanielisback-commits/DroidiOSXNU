# Motorola Moto G60

**Status: initial hardware research. No XNU port or device boot support is implemented.**

## Identity

- Commercial name: Motorola Moto G60
- Exact model reported by owner: `XT2135-2`
- Common platform codename: `hanoip` (also shared in public device trees with Moto G40 Fusion)
- Owner-confirmed RAM: 6 GB
- Owner-confirmed internal storage: 128 GB total, with 124 GB currently used
- Owner-reported software build: `S2RIS32.32-20-9-9-2-3`
- Matching Motorola Linux kernel release: `MMI-S2RIS32.32-20-9-9-2-3`
- SoC platform family in the matching source: Qualcomm SDM Magpie / SM6150
- GPU: Qualcomm Adreno 618 (reported in public Android device configuration)
- Board revision: not yet independently identified

The exact model, memory configuration, storage capacity/usage, and build string were supplied by the device owner. Motorola's kernel-source issue #574 names the exact XT2135-2 European firmware package and links to the matching kernel source release. This is a strong source baseline for the reported software build, but does not by itself prove the physical board ID or every replaceable component.

Public Android device trees identify `hanoip` as a shared Moto G40 Fusion/Moto G60 platform. The Moto G40 Fusion and Moto G60 have regional hardware differences, so do not assume every listed component or configuration is identical.

## Preliminary hardware inventory

| Subsystem | Research finding | Confidence / next check |
| --- | --- | --- |
| SoC | Qualcomm SDM Magpie / SM6150 platform family in matching kernel DTS | Exact-build source evidence; commercial chipset branding is a separate specification claim |
| CPU | ARM64 platform; octa-core Kryo 470 family reported | Confirm exact CPU topology from matching DTS/source |
| GPU | Adreno 618 reported in Android device configuration | Driver feasibility unknown |
| Display | Tianma ILI7807S 678, 1080 × 2460 panel definition; 60/120 Hz modes in matching DTS | Exact-build panel software definition; verify physical panel revision |
| Touchscreen | SPI node compatible with `tchip,ilitek` in matching DTS | Strong software-interface lead; retail controller revision unknown |
| Memory / storage | 6 GB RAM and 128 GB internal storage confirmed by owner; 124 GB currently used | Device-specific configuration confirmed |
| NFC | `qcom,nq-nci` I2C node in matching DTS | Software integration evidence; exact module not confirmed |
| Fingerprint | FPC1020-compatible node in matching DTS | Software configuration lead; verify fitted sensor |
| Sensors | Semtech SX933x node in matching DTS | Software configuration lead; exact role/part needs confirmation |
| Cameras | Matching DTS describes rear main, rear wide, rear depth and front camera paths | Exact sensor population/revision needs confirmation |
| Audio | Qualcomm Bolero/MI2S and audio-DSP integration references | Codec and full audio routing need confirmation |
| Wi-Fi / Bluetooth | Not conclusively identified in the exact-build DTS files reviewed so far | Chipset, firmware interface, and driver support unknown |
| Storage controller | UFS controller/PHY references in matching platform DTS | No XNU storage driver |
| Boot firmware | Exact XT2135-2 Android 12 software build recorded above | Boot-chain assumptions not yet inventoried |

Specifications above distinguish exact-build source declarations from general product specifications. A device-tree node is evidence of a configured software interface, not absolute proof of the exact physical component fitted in every production unit.

## Public source leads

- [Motorola EU declaration of conformity identifying XT2135-2 as Moto G60](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf)
- [Motorola Moto G60 product announcement (128 GB built-in storage)](https://motorolanews.com/ultra-high-res-photos-meet-ultra-fast-performance-introducing-moto-g60/)
- [Motorola kernel source release: exact build](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)
- [Motorola source publication record, issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)
- [Android device tree: motorola-sm6150-devs/android_device_motorola_hanoip](https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip)
- [Moto Hanoip community source organization](https://github.com/moto-hanoip/)
- [Secondary specification reference](https://www.notebookcheck.net/Motorola-Moto-G60.543352.0.html)
- [DroidiOSXNU public device-tree audit](../docs/MOTO_G60_DEVICE_TREE_AUDIT.md)
- [DroidiOSXNU exact-build kernel-source audit](../docs/MOTO_G60_KERNEL_SOURCE_AUDIT.md)

Review applicable licenses before any code reuse. The presence of Android/Linux device support does not establish XNU compatibility. DroidiOSXNU records findings and links only; it does not copy Motorola kernel code or proprietary vendor blobs.

## Next research tasks

- [x] Record exact model number, RAM, total storage, reported used storage, and software build as supplied by the device owner.
- [x] Confirm 128 GB storage capacity.
- [x] Review a public `hanoip` Android device tree.
- [x] Find and inspect the Motorola kernel source release matching the owner's exact software build.
- [x] Record exact-build display, touchscreen, NFC, fingerprint, sensor, camera-topology, audio and storage-controller source clues.
- [ ] Determine which `hanoip` board ID corresponds to the owner's physical XT2135-2.
- [ ] Resolve the touchscreen NVT-versus-Ilitek discrepancy between community and exact-build source trees.
- [ ] Identify WLAN/Bluetooth hardware and matching driver bindings.
- [ ] Build a host-side XNU platform bring-up and driver-gap plan.

## Safety and scope

This is static source research. Do not flash experimental images or modify boot partitions. Keep the phone's normal operating system intact. Do not publish serial numbers, IMEI values, account details, private logs, or proprietary firmware.

A working Android kernel/device tree is useful evidence about the hardware, but it is not a ready-made XNU port.
