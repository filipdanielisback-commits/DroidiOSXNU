# Architecture overview

DroidiOSXNU is currently a research plan, not a functioning port. The layers below describe areas to investigate; they are not claims that implementations exist.

## Research layers

1. **Host tools** — source checkouts, build orchestration, image inspection, and validation.
2. **Kernel research** — public XNU source revision, ARM64 configuration, required patches, and build reproducibility.
3. **Boot environment** — understand the device's documented boot chain and determine whether a safe, reversible development path exists.
4. **Platform description** — identify CPU topology, memory map, interrupts, timers, buses, and device-tree or ACPI information as applicable.
5. **Drivers** — assess display, input, storage, USB, networking, audio, GPU, sensors, and power-management support independently.
6. **Userspace compatibility** — investigate the boundary between an open XNU kernel and proprietary operating-system components. Do not assume the complete iOS userspace is available as source.

## Design principles

- Keep common code separate from per-device data.
- Prefer documented interfaces and upstream open-source components.
- Keep experiments reversible and avoid destructive device modifications.
- Never include secrets or proprietary firmware in source control.
- Record the exact source revision and license for every imported component.
- Treat all hardware support as unverified until tested on the named device.

## First milestone

Produce a hardware inventory for the Moto G60 and a host-side build/test plan. Do not begin by assuming that a kernel built for another phone can be reused unchanged.
