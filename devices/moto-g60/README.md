# Motorola Moto G60

**Status: initial hardware research. No XNU port or device boot support is implemented.**

## Identity

- Commercial name: Motorola Moto G60
- Exact model reported by owner: `XT2135-2`
- Common platform codename: `hanoip` (also shared in public device trees with Moto G40 Fusion)
- Owner-confirmed RAM: 6 GB
- Owner-confirmed internal storage: 128 GB total, with 124 GB currently used
- Owner-reported software build: `S2RIS32.32-20-9-9-2-3`
- Firmware package family identified in public references: `XT2135-2_HANOIP_RETEU_12_...` (European retail channel; Android 12)
- SoC: Qualcomm Snapdragon 732G / SM7150 family
- GPU: Qualcomm Adreno 618
- Board revision: not yet recorded

The exact model, memory configuration, storage capacity/usage, and build string were supplied by the device owner. Motorola's EU declaration identifies XT2135-2 as the Moto G60 model, and Motorola's product announcement lists 128 GB built-in storage. A Motorola kernel-source request associates the reported build with the XT2135-2 European hanoip firmware package. This helps identify the software baseline, but does not by itself verify every hardware component or guarantee that a particular kernel source snapshot exactly matches the installed binary.

Public Android device trees identify `hanoip` as the Moto G40 Fusion/Moto G60 platform. The Moto G40 Fusion and Moto G60 have regional hardware differences, so do not assume every listed component or configuration is identical.

## Preliminary hardware inventory

| Subsystem | Research finding | Confidence / next check |
| --- | --- | --- |
| SoC | Snapdragon 732G (SM7150 family) | Public platform lead; verify against exact board sources |
| CPU | Octa-core Kryo 470 family | Cross-check exact device variant |
| GPU | Adreno 618 | Public platform specification; driver feasibility unknown |
| Display | 6.8-inch IPS LCD, 1080 × 2460, up to 120 Hz reported | Panel/controller and display pipeline not identified |
| Memory / storage | 6 GB RAM confirmed by owner; 128 GB internal storage confirmed by owner; 124 GB currently used | Device-specific configuration confirmed; free space changes over time |
| Battery | 6,000 mAh reported | Not relevant to kernel compatibility by itself |
| Wi-Fi / Bluetooth | Dual-band Wi-Fi and Bluetooth 5.0 reported | Chipset, firmware interface, and driver support unknown |
| Audio | Speaker, earpiece, microphones, 3.5 mm audio reported | Codec, routing, and amplifier details unknown |
| Cameras | Regional variants differ; G60 commonly reported with 108 MP main camera, G40 Fusion with 64 MP | Do not assume camera modules are interchangeable |
| Touchscreen | Capacitive touch | Controller and Linux driver not yet identified |
| Boot firmware | Exact XT2135-2 Android 12 software build recorded above | Boot-chain details not yet inventoried |
| Sensors / power | Several standard phone sensors reported | Exact sensor parts and power-management devices unknown |

Specifications above are preliminary research leads, not a validated board-level bill of materials. Secondary specification sites can contain errors or combine regional variants.

## Public source leads

- [Motorola EU declaration of conformity identifying XT2135-2 as Moto G60](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf)
- [Motorola Moto G60 product announcement (128 GB built-in storage)](https://motorolanews.com/ultra-high-res-photos-meet-ultra-fast-performance-introducing-moto-g60/)
- [Android device tree: motorola-sm6150-devs/android_device_motorola_hanoip](https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip)
- [Android device tree: device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [Moto Hanoip community source organization](https://github.com/moto-hanoip/)
- [Motorola kernel source release discussion for hanoip](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/415)
- [Motorola kernel source request for the exact XT2135-2 build S2RIS32.32-20-9-9-2-3](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)
- [Secondary specification reference](https://www.notebookcheck.net/Motorola-Moto-G60.543352.0.html)

These are research references only. Review each repository's license and history before using any code. The presence of Android/Linux device support does not establish XNU compatibility.

## Next research tasks

- [x] Record exact model number, RAM, total storage, reported used storage, and software build as supplied by the device owner.
- [x] Confirm 128 GB storage capacity.
- [ ] Verify `hanoip` identity against device-specific public sources.
- [ ] Inspect public device-tree configuration and record component names with source links.
- [ ] Identify the exact display panel and touchscreen controller from documented sources.
- [ ] Identify Wi-Fi/Bluetooth, audio codec, camera, and sensor components.
- [ ] Locate and review the matching vendor kernel source release and its license.
- [ ] Build a host-side compatibility assessment; do not attempt a device boot yet.
- [ ] Record each finding as verified, tentative, or unknown.

## Safety and scope

Do not flash experimental images or modify boot partitions as part of this research phase. Keep the phone's normal operating system intact. Do not publish serial numbers, IMEI values, account details, private logs, or proprietary firmware.

A working Android kernel/device tree is useful evidence about the hardware, but it is not a ready-made XNU port.
