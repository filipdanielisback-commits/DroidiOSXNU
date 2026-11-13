# XNU ARM64 source integration and platform foundations

**Status:** source-integration tooling added; exact local checkout and pinned-file review pending  
**Upstream:** Apple `apple-oss-distributions/xnu`  
**Pinned tag:** `xnu-12377.121.6`  
**Pinned commit:** `ac9718fb1af618d5ce8678d0dc6e8a58f252216f`  
**Target:** Motorola Moto G60 XT2135-2 / `hanoip`, research only

## 1. What this milestone does

DroidiOSXNU now has a host-side fetch tool that checks out the exact Apple XNU revision recorded in `kernel/xnu-source-pin.json` into the ignored local path `kernel/upstream/xnu`. The tool verifies both the annotated tag object and the peeled commit before leaving a detached checkout.

The source is not copied into the DroidiOSXNU Git repository. This avoids silently maintaining a second copy of a large upstream tree and preserves a clear boundary between Apple's source and original project changes. The checkout retains Apple's original license and notices.

Run from the repository root:

```sh
python tools/fetch_xnu_source.py
```

The tool requires Git and network access to GitHub. It refuses to overwrite an existing non-Git destination, a working tree with local changes, or a working tree whose `origin` is not the Apple XNU repository. It does not build XNU, access a phone, or create a bootable artifact.

The checked-out source directory is intentionally ignored by Git. The pin metadata and the fetch tool are committed; the upstream source itself remains a separate local checkout.

## 2. ARM64 source areas to inspect

These are the first source files and directories to review in the exact pinned checkout. Links are pinned to the project's tag rather than to a moving branch.

| Source path | Foundation topic | What must be established from the pinned source |
|---|---|---|
| [`osfmk/arm64/start.s`](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/osfmk/arm64/start.s) | ARM64 entry and early architectural state | Entry assumptions, boot-argument contract, exception-level assumptions, early translation setup, and handoff to C initialization. |
| [`osfmk/arm/arm_init.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/osfmk/arm/arm_init.c) | Boot-CPU initialization | Platform-expert initialization, memory information inputs, VM initialization dependencies, CPU setup, and timebase initialization. |
| [`osfmk/arm64/sleh.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/osfmk/arm64/sleh.c) | ARM64 exception handling | Exception-vector expectations and the platform hooks used for architecture-specific error handling. |
| [`osfmk/arm64/proc_reg.h`](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/osfmk/arm64/proc_reg.h) | ARM64 system-register definitions | Which architectural features and register definitions are assumed by the selected configuration. |
| [`pexpert/arm64/board_config.h`](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/pexpert/arm64/board_config.h) | ARM64 platform configuration boundary | Which configuration values are generic, Apple-platform-specific, or selected at build time. |
| `osfmk/arm/`, `pexpert/arm/`, `pexpert/arm64/` | Architecture/platform boundary | Where generic ARM code ends and platform expert responsibilities begin. |

The links are navigation aids. The exact checked-out commit is authoritative. Do not copy or adapt code from the moving `main` branch in place of the pinned source.

## 3. Platform foundations: dependency order

The order below is a research and validation sequence, not a device boot procedure.

1. **Source provenance and build assumptions.** Verify the local checkout, source license, tag object, commit, configuration inputs, and compiler/SDK expectations.
2. **Entry contract.** Identify the boot CPU's expected exception level, register state, boot-argument format, memory ownership, and entry assumptions. The Moto G60's compatible handoff is currently unknown.
3. **Physical memory and MMU.** Map the exact target memory regions, reserved ranges, page granule, cacheability rules, and address-translation requirements against XNU's assumptions. No target map is validated.
4. **CPU features and topology.** Identify the actual CPU implementation, architectural features, core topology, and SMP contract. The platform evidence map is not sufficient to claim this.
5. **Exceptions and interrupts.** Identify the exception model, interrupt-controller contract, routing, and per-CPU behavior. No XNU interrupt-controller integration is implemented.
6. **Timers and timebase.** Establish the architectural timer source, frequency, interrupt delivery, and timekeeping requirements. No XNU timer integration is implemented.
7. **Platform expert boundary.** Only after the preceding facts are sourced should a target-specific platform layer be designed. No `hanoip` XNU platform layer exists today.

## 4. Evidence status for the Moto G60

| Foundation | Current evidence | Status |
|---|---|---|
| ARM64 source | Apple XNU documents ARM64 support; the project has a pinned source revision | Architecture overlap only |
| Entry / boot arguments | No compatible XNU handoff contract is documented for XT2135-2 | Unknown |
| Memory map / MMU | Motorola device-source clues exist, but no XNU-compatible runtime map is validated | Unverified |
| CPU features / SMP | Qualcomm source clues exist; exact XNU feature and CPU-start contract is not established | Unverified |
| Exceptions / interrupts | Platform declarations exist, but no XNU controller integration is present | Unimplemented |
| Timer / timebase | Platform clock/timer clues exist, but no XNU timebase implementation is present | Unimplemented |
| Platform expert | No Moto G60-specific XNU platform layer has been implemented | Unimplemented |

See [Moto G60 XNU platform evidence map](MOTO_G60_XNU_PLATFORM_EVIDENCE_MAP.md) and [XNU feasibility assessment](MOTO_G60_XNU_FEASIBILITY.md) for the source provenance and unresolved hardware questions.

## 5. What counts as real implementation

A file named after a device or a driver is not evidence of support. A future platform component must have:

- a pinned source and hardware evidence basis;
- a documented interface and explicit assumptions;
- original changes clearly separated from Apple's upstream files;
- a reproducible build or compile result for the exact configuration;
- tests appropriate to the component, with test scope stated;
- independent hardware-validation evidence before it is called hardware-working.

A host-side metadata test is not a kernel test. A successful compile is not a boot test. A source checkout is not a port.

## 6. Current result and next gate

**Completed in this repository:** an exact-revision source fetcher, its host-side tests, and this source-backed foundation review map.

**Not yet completed:** running the fetcher in the user's local Termux checkout, inspecting the exact pinned source files locally, validating a public build environment, implementing target platform code, compiling XNU, or testing hardware.

The next gate is to run the fetcher and inspect the pinned source files. Only after that review should we decide whether any original platform abstraction can be implemented without inventing hardware behavior.

## 7. Scope and safety

This milestone is limited to source checkout, source review, documentation, and host-side tests. It does not include bootloader changes, firmware extraction, flashing, partition changes, device installation, or any other modification to the phone.
