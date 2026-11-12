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

## Findings from the source configuration

| Area | What the source says | Interpretation / confidence |
| --- | --- | --- |
| Platform | `TARGET_BOARD_PLATFORM := sm6150`; QCOM platform family `sm6150` | Confirmed as the Android build target in this tree; not an XNU platform identifier |
| GPU | `TARGET_BOARD_PLATFORM_GPU := qcom-adreno618` | Android build configuration names Adreno 618 |
| CPU architecture | `TARGET_ARCH := arm64`, `TARGET_ARCH_VARIANT := armv8-a` | ARM64 / Armv8-A target configuration |
| Kernel build reference | `TARGET_KERNEL_SOURCE := kernel/motorola/sm6150`; `TARGET_KERNEL_CONFIG := vendor/hanoip_defconfig` | Identifies the expected Android kernel source path and defconfig in that Android build environment; source itself was not audited here |
| Boot image metadata | Header version 3; 4096-byte kernel pages; separate DTBO enabled | Android boot-image build settings, not instructions for modifying the phone |
| WLAN | `BOARD_WLAN_DEVICE := qcwcn`; `WIFI_DRIVER_DEFAULT := qca_cld3`; config copied to a `qca6390` directory | Qualcomm WLAN software stack/config references. Do not infer an exact physical chip solely from these names |
| Audio | Module aliases include WCD934x, WCD937x, WSA881x and Qualcomm audio DSP components | Shows the Android tree accounts for Qualcomm audio modules; the alias list alone does not prove which optional codec/module is populated in this exact phone |
| Touch | `TARGET_TAP_TO_WAKE_NODE := /sys/class/touchscreen/NVT-ts/double_click` | Strong source hint for an NVT touchscreen sysfs interface in this tree; exact controller/part number remains unverified |
| Display | Android config enables HWC2, Qualcomm display/gralloc components, ION and Vulkan | Identifies Android graphics stack choices, not the exact LCD panel or a reusable XNU driver |
| Fingerprint | Config references both EGIS and FPC input/key-layout files | Multiple support paths are present; exact sensor vendor on the owner's unit remains unknown |
| NFC | Device manifest includes Android NFC and NXP NFC interfaces | Software integration evidence; exact module and regional availability still need confirmation |
| Sensors | Android sensor HAL packages are included | Does not identify individual sensor part numbers |

## Important cautions

1. **Shared-device-tree limitation:** `hanoip` includes both G40 Fusion and G60. The product file in this snapshot even labels the model as G40 Fusion. Treat the tree as a source of leads, not proof of the XT2135-2 bill of materials.
2. **Android is not XNU:** Android HALs, vendor modules, init scripts, SELinux policy, and proprietary libraries cannot simply be used as XNU drivers.
3. **No proprietary extraction:** Do not copy vendor blobs, firmware, calibration data, keys, or proprietary files into this repository.
4. **No boot experiments:** This audit does not authorize flashing, unlocking, partition changes, security changes, or experimental boot attempts. Keep the phone's normal software intact.
5. **Configuration warnings:** This Android tree contains Android-specific build settings, including a permissive SELinux build flag. These are not recommendations and must not be carried over into DroidiOSXNU.

## What this tells us about XNU feasibility

- The target is an ARM64 Qualcomm platform, so CPU architecture is not the first unknown.
- The largest unresolved work is platform bring-up: interrupt controller, timers, SMP, memory map, clocks, regulators, power management, storage, USB, display, touch, audio, WLAN, Bluetooth, sensors, and modem integration.
- Existing Android support is evidence that the hardware has been brought up under Linux/Android. It does not establish that XNU has the required platform drivers or interfaces.
- A realistic next phase is a source-only inventory of the matching Linux kernel and device-tree sources, recording component names and licensing without copying implementation code.

## Next research checklist

- [x] Review a public `hanoip` device tree's board configuration and product configuration.
- [ ] Compare this tree's source references with the exact XT2135-2 build and the matching Motorola kernel-source release.
- [ ] Identify the actual touchscreen, WLAN, audio, fingerprint, NFC, and sensor components from reliable model-specific sources.
- [ ] Inspect the kernel device-tree source for compatible strings and record only sourced findings.
- [ ] Start an XNU-versus-Linux driver gap matrix; keep unknowns explicit.
