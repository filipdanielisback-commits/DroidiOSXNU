# Boot research

This directory is reserved for documentation and original, reviewed code related to the experimental boot environment.

No bootloader or device-boot implementation is present. First document the Moto G60's exact variant, documented boot chain, and safe/reversible development options. Do not assume that procedures for another device apply here.

## Current prototype

The first architecture prototype is deliberately host-only:

- [Boot-flow simulator design](../docs/BOOT_FLOW_SIMULATOR.md)
- [Host-side simulator](../tools/boot_flow_simulator.py)

It models planning stages and reporting only. It does not inspect a phone, communicate with a bootloader, load a kernel, modify storage, or generate an image. A completed simulation is not a successful boot test.
