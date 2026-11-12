# Moto G60 WLAN and Bluetooth research

**Status: preliminary software-stack clues only. The exact physical WLAN/Bluetooth combo chip is not confirmed.**

## Scope and source hierarchy

The primary baseline remains Motorola's kernel source release matching the owner's reported build `S2RIS32.32-20-9-9-2-3`:

- [Motorola kernel release](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)
- [Motorola source publication issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)

A search of the available exact-build DTS review did not establish a WLAN or Bluetooth silicon identifier. The following clues come from a separate public community Android device tree for the shared `hanoip` family, not from a confirmed physical teardown or an exact-build chip declaration:

- [Community Hanoip device tree](https://github.com/bhawesh2002/android_device_motorola_hanoip/)
- [BoardConfig.mk](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/ec92d37ee6fa659294efaf170f2df2ea4f6d7398/BoardConfig.mk)
- [device.mk](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/ec92d37ee6fa659294efaf170f2df2ea4f6d7398/device.mk)
- [init.target.rc](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/ec92d37ee6fa659294efaf170f2df2ea4f6d7398/rootdir/etc/init.target.rc)
- [ueventd.qcom.rc](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/ec92d37ee6fa659294efaf170f2df2ea4f6d7398/rootdir/etc/ueventd.qcom.rc)

## Findings

| Area | Community-tree clue | What it supports | What it does not prove |
| --- | --- | --- | --- |
| WLAN build configuration | `BOARD_WLAN_DEVICE := qcwcn`, `WIFI_DRIVER_DEFAULT := qca_cld3` | Qualcomm WLAN software stack and CLD3 driver family are used in that tree | Exact radio chip fitted to this XT2135-2 unit |
| WLAN module names | References include `qca_cld3_wlan.ko`, `qca_cld3_qca6390`, and `qca_cld3_qca6490` | The device configuration contains Qualcomm CLD3-related driver integration | That all listed modules are for this phone or that QCA6390/QCA6490 is the installed chip |
| WLAN device interface | `/dev/wcnss_wlan`, `/dev/wcnss_ctrl`, and a `qcom,wcnss-wlan` sysfs path appear in init/uevent rules | The Android stack includes WCNSS-named interfaces in this source snapshot | The exact transport, firmware revision, or physical combo module |
| Bluetooth | Qualcomm Bluetooth stack selection and Bluetooth audio/SAR HAL references | Qualcomm-specific Android Bluetooth integration is present | Bluetooth controller model, bus wiring, or a matching XNU driver |

### Important inconsistency

The community tree mixes older-looking WCNSS interface references with newer CLD3/QCA6390/QCA6490 module and configuration names. It may contain compatibility aliases, inherited configuration, or support for more than one platform revision. It is therefore unsafe to select one chipset name as the definitive hardware identity.

The exact-build Motorola source should take precedence over generic community configuration when it provides a specific declaration. Until an exact-build DTS node, authoritative component record, or reliable physical part identification is available, record WLAN and Bluetooth silicon as **unknown**.

## XNU implications

Android/Linux support is not directly reusable as an XNU driver. The project still needs independent research for:

- the radio's actual PCIe/SDIO/UART or other host interface and power/reset dependencies;
- firmware-loading and calibration requirements, without copying proprietary firmware into this repository;
- Bluetooth controller transport and power sequencing;
- XNU networking and Bluetooth framework integration;
- a legally compatible driver implementation or a documented statement that the subsystem is unsupported.

No driver code has been written. No firmware, calibration data, device dumps, keys, or proprietary blobs are included.

## Next checks

- [ ] Search the exact Motorola release's source/configuration for WLAN and Bluetooth platform declarations.
- [ ] Correlate any candidate chip ID with an authoritative XT2135-2 parts record; do not infer it from a shared `hanoip` tree.
- [ ] Keep WLAN and Bluetooth marked unknown until the evidence agrees.
- [ ] Add a subsystem-by-subsystem XNU driver-gap table after the hardware identity is established.

## Safety and scope

This is documentation-only source research. No device flashing, boot-chain modification, firmware extraction, or hardware changes are part of this milestone.
