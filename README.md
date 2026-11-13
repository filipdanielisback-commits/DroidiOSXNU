# DroidiOSXNU

**Experimental research into Apple's open-source XNU/Darwin kernel on Android hardware.**

The first device under investigation is the **Motorola Moto G60**. This repository is a research scaffold: it does not currently contain a working iOS port, a bootable image, or device drivers.

> **Status: early research — nothing here should be considered boot-ready.**

## Goals

- Study the public XNU source and document the compatibility work needed for ARM64 Android hardware.
- Inventory the Moto G60 hardware and its existing open-source platform support.
- Build reproducible research tools and tests before attempting device bring-up.
- Keep device-specific work separate so future ports can be evaluated independently.
- Investigate IPSW metadata and user-supplied firmware workflows without redistributing Apple's proprietary files.

## Device roadmap

| Device | Codename / platform | Status |
| --- | --- | --- |
| Motorola Moto G60 | To be verified from device inventory | **Initial research target** |
| Redmi Note 13 Pro 5G | To be verified | Planned research |
| POCO X5 5G | To be verified | Planned research |
| POCO X6 Pro 5G | To be verified | Planned research |
| Google Pixel 4a | To be verified | Planned research |
| Redmi Note 10 Pro | To be verified | Planned research |

Device support is not implied by appearing in this table. Each port needs its own hardware inventory, boot-chain analysis, driver assessment, and test results.

## Project layout

- `docs/` — architecture, research notes, roadmap, and legal boundaries.
- `devices/` — per-device research and configuration notes.
- `kernel/` — planned XNU integration notes and original patches.
- `boot/` — boot-flow research and host-only simulation.
- `gui/` — non-operational desktop GUI prototypes for research workflows.
- `drivers/` — hardware-driver research and original implementations.
- `tools/` — small, auditable development utilities.
- `ipsw/` — documentation for inspecting user-supplied firmware packages.
- `tests/` — host-side checks and future compatibility tests.

## Important technical reality

XNU is open source; the complete iOS operating system is not. Publishing XNU source does not provide the proprietary iOS frameworks, services, drivers, signing material, or a complete iOS source tree. An IPSW is a firmware distribution package, not source code.

The initial milestone is an independently buildable research environment and a documented hardware inventory—not a promise to boot iOS 26.2 on the Moto G60. Any iOS-version compatibility claim must be backed by verified public source revisions and repeatable tests.

## Firmware and legal boundaries

- Do not commit IPSW files, extracted proprietary firmware, keys, certificates, personal data, or device dumps.
- Do not include Apple's proprietary iOS binaries or claim they are open source.
- Keep third-party code and notices intact; review each component's license before importing or modifying it.
- Use firmware references such as [IPSW.me](https://ipsw.me/) as a catalog only. Users are responsible for obtaining firmware through legitimate channels and complying with applicable terms.
- This project is independent and is not affiliated with or endorsed by Apple, Motorola, Xiaomi, Google, or Qualcomm.

See [Legal and firmware policy](docs/LEGAL.md), [Architecture](docs/ARCHITECTURE.md), [Boot Manager GUI prototype](docs/BOOT_MANAGER_GUI.md), and [Roadmap](docs/ROADMAP.md).

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Research notes should distinguish verified facts, hypotheses, and unknowns. No hardware compatibility claim should be marked working without a reproducible test.

## License

A repository-wide license has not yet been selected. Until a license is added, do not assume that the project grants permission to reuse its original contents. Third-party components retain their own licenses.
