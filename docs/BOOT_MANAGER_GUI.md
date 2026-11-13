# Boot Manager GUI prototype

The first GUI milestone is a browser-based, host-only visual prototype at [gui/boot-manager/index.html](../gui/boot-manager/index.html).

## What it demonstrates

- A desktop-style research dashboard for the Moto G60 profile.
- Three illustrative stages: static profile display, compatibility review, and simulation summary.
- A local-only button interaction that updates the page's status text.
- Explicit unknown and not-implemented labels for hardware and XNU support.
- A visible warning that the interface is not a bootloader or installer.

## Run it on Windows 11 x64

Open `gui/boot-manager/index.html` in a current web browser. No phone, driver, administrator permission, Python package, USB connection, firmware file, or network service is required.

## Non-operational boundary

This prototype is ordinary browser UI. It does not communicate with Android, a bootloader, USB devices, storage, partitions, firmware, or a kernel. It contains no flashing, installation, recovery, unlock, or device-control feature. Its simulated progress is fictional and must not be reported as a hardware test or proof of compatibility.

The GUI is not itself a bootloader. It does not create or configure a bootable image. Any future research image must remain inert data-only content and must not contain executable boot code, a boot sector, partition table, filesystem, or device installation workflow.
