# Moto G60 (XT2135-2) — public device-tree audit

**Status: source review only. This is not an XNU port, a validated hardware bill of materials, or a boot procedure.**

## Target device

The project owner's test device is recorded as:

- Model: Motorola Moto G60, XT2135-2
- RAM: 6 GB
- Internal storage: 128 GB (124 GB reported used at the time of recording)
- Software build: `S2RIS32.32-20-9-9-2-3`

## Sources reviewed

The following public Android device-tree repository was inspected:

- Repository: [bhawesh2002/android_device_motorola_hanoip](https://github.com/bhawesh2002/android_device_motorola_hanoip)
- [README.md](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/README.md)
- [BoardConfig.mk](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/BoardConfig.mk)
- [device.mk](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/device.mk)
- [aosp_hanoip.mk](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/aosp_hanoip.mk)
- [manifest_hanoip.xml](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/manifest_hanoip.xml)

The README describes a combined Moto G(40) Fusion / Moto G(60) device target called `hanoip`. The product makefile in this snapshot sets `PRODUCT_MODEL := moto g(40) fusion`, so this tree is shared across variants and is not proof that every setting exactly matches the owner's XT2135-2.

The more important reference is now the [matching Motorola kernel-source release](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3), which is explicitly tied to the owner's exact software build. Its detailed findings are recorded in the [exact-build kernel-source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md).

## Findings from the community source configuration

| Area | What the source says | Interpretation / confidence |
| --- | --- | --- |
| Platform | `TARGET_BOARD_PLATFORM := sm6150`; QCOM platform family `sm6150` | Android build target; not an XNU platform identifier |
| GPU | `TARGET_BOARD_PLATFORM_GPU := qcom-adreno618` | Android build configuration names Adreno 618 |
| CPU architecture | `TARGET_ARCH := arm64`, `TARGET_ARCH_VARIANT := armv8-a` | ARM64 / Armv8-A target configuration |
| Kernel build reference | `TARGET_KERNEL_SOURCE := kernel/motorola/sm6150`; `TARGET_KERNEL_CONFIG := vendor/hanoip_defconfig` | Expected Android kernel source path and defconfig in that build environment |
| Boot image metadata | Header version 3; 4096-byte kernel pages; separate DTBO enabled | Android boot-image build settings, not instructions for modifying the phone |
| WLAN | `BOARD_WLAN_DEVICE := qcwcn`; `WIFI_DRIVER_DEFAULT := qca_cld3`; config copied to a `qca6390` directory | Qualcomm WLAN software-stack references. Do not infer an exact physical chip solely from these names |
| Audio | Module aliases include WCD934x, WCD937x, WSA881x and Qualcomm audio DSP components | Android audio-module support paths; exact populated codec/module still needs confirmation |
| Touch | `TARGET_TAP_TO_WAKE_NODE := /sys/class/touchscreen/NVT-ts/double_click` | Community-tree NVT sysfs hint; conflicts with the exact-build Motorola kernel DTS, which declares an Ilitek-compatible SPI touchscreen |
| Display | Android config enables HWC2, Qualcomm display/gralloc components, ION and Vulkan | Android graphics-stack choices; not an XNU driver |
| Fingerprint | Config references both EGIS and FPC input/key-layout files | Multiple support paths; exact fitted sensor needs confirmation |
| NFC | Device manifest includes Android NFC and NXP NFC interfaces | Software integration evidence; exact module and regional availability still need confirmation |
| Sensors | Android sensor HAL packages are included | Does not identify individual sensor part numbers |

## Important cautions

1. **Shared-device-tree limitation:** `hanoip` includes both G40 Fusion and G60. The product file in this snapshot even labels the model as G40 Fusion. Treat this tree as a source of leads, not proof of the XT2135-2 bill of materials.
2. **Touchscreen source conflict:** The community tree's NVT sysfs path is not consistent with the exact-build Motorola kernel DTS, which declares `tchip,ilitek` over SPI. The exact-build source is the stronger lead for this software build, but the physical controller/revision remains to be confirmed. See [kernel-source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md).
3. **Android is not XNU:** Android HALs, vendor modules, init scripts, SELinux policy, and proprietary libraries cannot simply be used as XNU drivers.
4. **No proprietary extraction:** Do not copy vendor blobs, firmware, calibration data, keys, or proprietary files into this repository.
5. **No boot experiments:** This audit does not authorize flashing, unlocking, partition changes, security changes, or experimental boot attempts. Keep the phone's normal software intact.
6. **Configuration warnings:** This Android tree contains Android-specific build settings, including a permissive SELinux build flag. These are not recommendations and must not be carried over into DroidiOSXNU.

## What this tells us about XNU feasibility

- The target is an ARM64 Qualcomm platform, so CPU architecture is not the first unknown.
- The largest unresolved work is platform bring-up: interrupt controller, timers, SMP, memory map, clocks, regulators, power management, storage, USB, display, touch, audio, WLAN, Bluetooth, sensors, and modem integration.
- Existing Android support is evidence that the hardware has been brought up under Linux/Android. It does not establish that XNU has the required platform drivers or interfaces.
- A matching Linux kernel source release is available for the owner's exact software build. This provides a source baseline for static analysis, not a ready-made XNU port.

## Next research checklist

- [x] Review a public `hanoip` device tree's board configuration and product configuration.
- [x] Compare its source references with the exact XT2135-2 build and locate the matching Motorola kernel-source release.
- [x] Inspect matching kernel device-tree source for peripheral compatible strings; see [exact-build kernel-source audit](MOTO_G60_KERNEL_SOURCE_AUDIT.md).
- [x] Record the touchscreen discrepancy rather than assuming the controller identity.
- [ ] Identify WLAN/Bluetooth hardware and matching driver bindings.
- [ ] Determine the board ID corresponding to the owner's physical XT2135-2.
- [ ] Continue the XNU-versus-Linux driver gap matrix with unknowns clearly marked.
