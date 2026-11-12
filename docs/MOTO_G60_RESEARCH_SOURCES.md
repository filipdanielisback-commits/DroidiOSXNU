# Moto G60 hardware research sources

This page tracks the public references used by the preliminary [Moto G60 device inventory](../devices/moto-g60/README.md).

## Primary and project sources

| Source | Why it matters | Limitation |
| --- | --- | --- |
| [Motorola support: Moto G60 hardware overview](https://motorola-mobility-en-in--dev3.custhelp.com/app/answers/detail/a_id/159299) | Manufacturer support page identifying external hardware and ports | Does not provide a complete board-level component inventory |
| [motorola-sm6150-devs Android device tree](https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip) | Public Android configuration for Moto G40 Fusion / Moto G60 (`hanoip`) | Community-maintained; inspect branch, commits, and license |
| [device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip) | Additional device configuration and integration references | Android configuration is not XNU support |
| [moto-hanoip organization](https://github.com/moto-hanoip/) | Historical device-source collection, including kernel-related repositories | Organization is archived; sources may be outdated |
| [Motorola kernel source issue #415](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/415) | Records a vendor kernel source release for a hanoip software build | Match the release to the exact device software version |
| [Notebookcheck Moto G60 specifications](https://www.notebookcheck.net/Motorola-Moto-G60.543352.0.html) | Secondary cross-check for marketed specifications | Not a substitute for board-level identification |

## Preliminary findings

Public Android device-tree descriptions associate Moto G60 with the `hanoip` platform and Qualcomm Snapdragon 732G / SM7150 family. A community device specification also lists Adreno 618 graphics. Motorola's support page documents the phone's external hardware layout.

Regional differences matter: Moto G60 and Moto G40 Fusion are closely related and share the `hanoip` platform name in public sources, but camera configurations and other parts may differ. The exact target unit must be identified before treating any component list as definitive.

## Evidence labels

- **Verified for a named unit** — observed on the exact device or confirmed by authoritative device-specific documentation.
- **Public-source lead** — described by a public device tree, source release, or credible specification reference, but not yet verified on the target unit.
- **Unknown** — not yet established.

Do not promote a public-source lead to verified hardware support without checking the exact variant and citing the evidence.
