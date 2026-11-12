# Motorola Moto G60

**Status: initial hardware research. No XNU port or device boot support is implemented.**

## Identity

- Commercial name: Motorola Moto G60
- Common platform codename: `hanoip` (also shared in public device trees with Moto G40 Fusion)
- SoC: Qualcomm Snapdragon 732G / SM7150 family
- GPU: Qualcomm Adreno 618
- Exact regional/model variant: must be confirmed on the actual target device before any device-specific work
- Board revision and installed software build: not yet recorded

Public Android device trees identify `hanoip` as the Moto G40 Fusion/Moto G60 platform. The Moto G40 Fusion and Moto G60 have regional hardware differences, so do not assume every listed component or configuration is identical.

## Preliminary hardware inventory

| Subsystem | Research finding | Confidence / next check |
| --- | --- | --- |
| SoC | Snapdragon 732G (SM7150 family) | Confirm against exact model and public board sources |
| CPU | Octa-core Kryo 470 family | Cross-check exact device variant |
| GPU | Adreno 618 | Public platform specification; driver feasibility unknown |
| Display | 6.8-inch IPS LCD, 1080 × 2460, up to 120 Hz reported | Panel/controller and display pipeline not identified |
| Memory / storage | Market configurations reported as 4/6 GB RAM and 64/128 GB storage | Confirm actual unit |
| Battery | 6,000 mAh reported | Not relevant to kernel compatibility by itself |
| Wi-Fi / Bluetooth | Dual-band Wi-Fi and Bluetooth 5.0 reported | Chipset, firmware interface, and driver support unknown |
| Audio | Speaker, earpiece, microphones, 3.5 mm audio reported | Codec, routing, and amplifier details unknown |
| Cameras | Regional variants differ; G60 commonly reported with 108 MP main camera, G40 Fusion with 64 MP | Do not assume camera modules are interchangeable |
| Touchscreen | Capacitive touch | Controller and Linux driver not yet identified |
| Boot firmware | Not yet inventoried | Research documented boot chain for exact variant |
| Sensors / power | Several standard phone sensors reported | Exact sensor parts and power-management devices unknown |

Specifications above are preliminary research leads, not a validated board-level bill of materials. Secondary specification sites can contain errors or combine regional variants.

## Public source leads

- [Motorola support: Moto G60 hardware overview](https://motorola-mobility-en-in--dev3.custhelp.com/app/answers/detail/a_id/159299)
- [Android device tree: motorola-sm6150-devs/android_device_motorola_hanoip](https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip)
- [Android device tree: device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [Moto Hanoip community source organization](https://github.com/moto-hanoip/)
- [Motorola kernel source release discussion for hanoip](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/415)
- [Secondary specification reference](https://www.notebookcheck.net/Motorola-Moto-G60.543352.0.html)

These are research references only. Review each repository's license and history before using any code. The presence of Android/Linux device support does not establish XNU compatibility.

## Next research tasks

- [ ] Confirm exact model number, region, RAM/storage configuration, and software build from the target unit.
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
