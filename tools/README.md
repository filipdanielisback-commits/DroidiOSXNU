# Development tools

This directory contains small, auditable host-side utilities for source verification, metadata inspection, build orchestration, and test-report validation.

## Device Tree inventory

Run the best-effort DTS/DTSI text inventory with Python 3 (standard library only):

```sh
python3 tools/dts_inventory.py path/to/source.dts path/to/include-directory
python3 tools/dts_inventory.py path/to/device-tree --format csv -o inventory.csv
```

The tool extracts node paths and the `compatible`, `reg`, and `status` properties into JSON (default) or CSV. It reads only files explicitly supplied or found below supplied directories; it does not fetch sources, inspect a connected phone, or modify inputs.

**Limitations:** this is a lightweight text inventory, not a Device Tree compiler. It does not resolve `/include/`, `#include`, overlays, labels, macros, phandles, or parent bus address-cell rules. A missing `status` property is left blank (Device Tree's default is generally `okay`). Use the Device Tree Compiler (`dtc`) and binding documentation for syntax and semantic validation. Review output before treating it as hardware fact.

## Boot-flow simulator

Run the host-only architecture simulation from the repository root:

```sh
python3 tools/boot_flow_simulator.py
python3 tools/boot_flow_simulator.py --list-stages
python3 tools/boot_flow_simulator.py --json
python3 tools/boot_flow_simulator.py --fail-at kernel_plan
```

It reports illustrative planning stages and can inject a fictional block to exercise status reporting. It does not load or execute a kernel, inspect hardware, access a bootloader, read/write device storage, or create a boot image. See [the simulator design](../docs/BOOT_FLOW_SIMULATOR.md).

Tools must not download or redistribute proprietary iOS binaries, handle private signing keys, or attempt to bypass platform security controls. Document inputs, outputs, dependencies, and tests for each tool.
