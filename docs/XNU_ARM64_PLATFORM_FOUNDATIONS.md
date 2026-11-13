# XNU ARM64 source integration and platform foundations

**Status:** exact local source checkout verified; initial ARM64 source inspection completed; platform implementation not started  
**Upstream:** Apple `apple-oss-distributions/xnu`  
**Pinned tag:** `xnu-12377.121.6`  
**Pinned commit:** `ac9718fb1af618d5ce8678d0dc6e8a58f252216f`  
**Target:** Motorola Moto G60 XT2135-2 / `hanoip`, research only

## 1. What this milestone does

DroidiOSXNU has a host-side fetch tool that checks out the exact Apple XNU revision recorded in `kernel/xnu-source-pin.json` into the ignored local path `kernel/upstream/xnu`. The tool verifies both the annotated tag object and the peeled commit before leaving a detached checkout.

The local Termux checkout was successfully fetched. The user verified that `git -C kernel/upstream/xnu rev-parse HEAD` prints the exact pinned commit above, and `git -C kernel/upstream/xnu status --short` printed no output. The source directory was therefore clean at the time of inspection.

The source is not copied into the DroidiOSXNU Git repository. This avoids silently maintaining a second copy of a large upstream tree and preserves a clear boundary between Apple's source and original project changes. The checkout retains Apple's original license and notices.

Run from the repository root:

```sh
python tools/fetch_xnu_source.py
```

The tool requires Git and network access to GitHub. It refuses to overwrite an existing non-Git destination, a working tree with local changes, or a working tree whose `origin` is not the Apple XNU repository. It does not build XNU, access a phone, or create a bootable artifact.

The checked-out source directory is intentionally ignored by Git. The pin metadata and the fetch tool are committed; the upstream source itself remains a separate local checkout.

## 2. ARM64 source areas inspected

The following observations were made against the user's local checkout of the exact pinned revision. The line numbers below are the line numbers shown by the local grep output and are navigation hints; the pinned commit is authoritative.

| Source path | Observed evidence | What it establishes — and what it does not |
|---|---|---|
| `osfmk/arm64/start.s` | Includes ARM64 assembly/register headers, `pexpert/arm64/board_config.h`, and exception assembly definitions. Defines macros that write `VBAR_EL1`, `TCR_EL1`, `TTBR1_EL1`, and `SCTLR_EL1`. Its comments describe a reset-handler handoff using boot-argument and CPU-data pointers. | Apple's ARM64 startup path uses architecture registers and a platform-configuration interface. This does not establish that the Moto G60 supplies a compatible entry environment or boot-argument contract. |
| `osfmk/arm64/arm_vm_init.c` | Includes `vm/pmap.h`; contains physical/virtual address helpers, page-table mapping helpers, exception-vector mapping preparation, page-granular permission helpers, TLB-flush references, and `arm_vm_prot_init()`. | XNU VM initialization is integrated with pmap, translation tables, exception-vector mappings, and page protections. No Moto G60 memory map or MMU configuration has been validated. |
| `osfmk/arm64/sleh.c` | Declares synchronous, IRQ, FIQ, SError and invalid-stack handlers; user/kernel abort handlers; VM fault helpers; and PAC/BTI/SME trap handlers. Includes Mach exception, VM fault, and platform error-handler interfaces. | ARM64 exception handling is connected to Mach, VM, thread state, and platform error handling. The grep output does not demonstrate interrupt-controller or platform integration for hanoip. |
| `pexpert/pexpert/arm64/board_config.h` | Contains conditional Apple platform configurations such as T6000, T6020, T8101, T8103, T8112, T8122/T8130, T8132, T8142, and T6030. Example configuration macros cover CPU counts/clusters, physical-address-space options, Apple SMP selection, memory-protection features, and platform error handling. | The header illustrates a distinct platform-configuration layer above generic ARM64 code. A targeted search found no Qualcomm, Snapdragon, SM6150, SM7150, Magpie, or Hanoip strings in this header. That negative result applies only to this file, not the entire XNU tree. |

### Header include-path clarification

The include written in `start.s` is:

```c
#include <pexpert/arm64/board_config.h>
```

The corresponding repository file found in the checkout is:

`pexpert/pexpert/arm64/board_config.h`

The additional directory level is resolved through the build system's include paths. The repository-root-relative path should not be guessed from the include spelling alone.

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
| ARM64 source | Apple XNU contains ARM64 startup, VM, and exception-handling source; the project has a pinned source revision | Architecture overlap only |
| Entry / boot arguments | Startup source uses boot-argument and CPU-data interfaces, but no compatible XNU handoff contract is documented for XT2135-2 | Unknown |
| Memory map / MMU | XNU source has pmap and translation-table machinery; Motorola device-source clues exist, but no XNU-compatible runtime map is validated | Unverified |
| CPU features / SMP | Apple's board header shows platform-specific CPU configuration patterns; Qualcomm source clues exist, but exact XNU feature and CPU-start contract is not established | Unverified |
| Exceptions / interrupts | XNU has ARM64 exception handlers; no XNU controller integration for the target is present | Unimplemented |
| Timer / timebase | Platform clock/timer clues exist, but no XNU timebase implementation is present | Unimplemented |
| Platform expert | The inspected Apple header contains Apple platform conditionals; no Moto G60-specific XNU platform layer has been implemented | Unimplemented |

See [Moto G60 XNU platform evidence map](MOTO_G60_XNU_PLATFORM_EVIDENCE_MAP.md) and [XNU feasibility assessment](MOTO_G60_XNU_FEASIBILITY.md) for source provenance and unresolved hardware questions.

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

**Completed:** exact-revision source fetcher; synthetic fetcher tests; local fetch success; exact commit verification; clean-checkout verification; initial inspection of ARM64 startup, VM initialization, exception handling, and board-configuration source.

**Not completed:** full boot-contract analysis; target CPU-feature or topology validation; interrupt-controller or timer integration; public build-environment validation; target platform code; XNU compilation; hardware testing.

The next research gate is a deeper, source-backed read of the startup handoff and the generic ARM initialization path, followed by CPU/topology and interrupt/timebase dependency mapping. Any conclusions must be recorded as confirmed, unresolved, or unknown. Do not infer target behavior from generic ARM64 support.

## 7. Scope and safety

This milestone is limited to source checkout, source review, documentation, and host-side tests. It does not include bootloader changes, firmware extraction, flashing, partition changes, device installation, or any other modification to the phone.
