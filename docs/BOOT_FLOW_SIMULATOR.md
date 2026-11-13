# Host-only boot-flow simulator

## Purpose

The simulator provides a small, repeatable way to discuss the *shape* of a
future boot architecture without implementing a bootloader or interacting
with a phone. It is a reporting and test fixture for development planning.

## Modeled stages

1. **Environment** — placeholder for documenting host-side prerequisites.
2. **Configuration** — placeholder for reviewing a platform configuration.
3. **Kernel plan** — placeholder for tracking XNU integration readiness.
4. **Platform plan** — placeholder for tracking platform and driver readiness.
5. **Handoff** — a conceptual endpoint only; no executable handoff occurs.

Every successful stage is labeled `SIMULATED`. The optional `--fail-at`
argument injects a fictional block so the reporting path can be tested.
It does not probe or diagnose a real system.

## Run on a development host

From the repository root:

```sh
python3 tools/boot_flow_simulator.py
python3 tools/boot_flow_simulator.py --list-stages
python3 tools/boot_flow_simulator.py --json
python3 tools/boot_flow_simulator.py --fail-at kernel_plan
python3 -m unittest discover -s tests -v
```

Python 3 standard library only; no third-party packages are required.

## Explicit non-goals and safety properties

- Does not open device interfaces or inspect a connected phone.
- Does not read or write partitions, firmware, boot variables, or storage.
- Does not unlock, configure, or communicate with a bootloader.
- Does not load, compile, link, or execute XNU or any kernel payload.
- Does not create a disk image, boot image, installer, or flashable artifact.
- Does not claim that any stage is implemented on the Moto G60.

A `SIMULATION_COMPLETE` result means only that the reporting routine ran
through its illustrative stages. It is not evidence of boot compatibility,
hardware support, or a working operating system.
