# DroidXNU architecture overview

DroidXNU's intended foundation is the public **XNU kernel source**. This document describes the architecture the research is organized around; it does not claim that any target-specific layer or working system exists.

## Reference architecture

The HakiOS project demonstrates one public way to organize XNU-on-Android research: a common kernel/tools layer, separate SoC and device descriptions, and a distinct QEMU research target. DroidXNU uses those separation principles as an architectural reference, not as a source of assumed-compatible code.

1. **Upstream XNU baseline** — exact public repository, tag, commit, license, and source provenance.
2. **Common kernel research** — generic XNU architecture and interfaces that are not specific to one phone.
3. **SoC/platform research** — CPU topology, interrupt and timer interfaces, memory layout, buses, clocks, power domains, and DMA/IOMMU facts.
4. **Device profile** — board- and model-specific facts, source provenance, confidence, and unresolved hardware identities.
5. **Driver research** — subsystem-by-subsystem mapping of existing public interfaces and missing XNU support.
6. **Userspace boundary** — separate study of what a usable system needs beyond the kernel; public XNU is not the complete iOS system.
7. **Host-side validation** — static validators, synthetic tests, and research simulations. A host test is not a phone compatibility test.

## Separation rules

- Keep upstream XNU metadata and any future common-kernel work separate from per-device information.
- Keep SoC-family facts separate from board- and model-specific facts.
- Do not infer that two devices are compatible because they share a codename or marketed chipset family.
- Track every hardware statement with a source and confidence level.
- Keep unknown or conflicting information explicitly unresolved.
- Review source provenance and licensing before considering external code reuse.

## What exists today

- A pinned public XNU source baseline and host-side metadata verifier.
- A Moto G60 platform profile and static device-tree/kernel-source research.
- A platform dependency inventory and XNU driver-gap matrix.
- Static feasibility and XNU-versus-iOS boundary reports.
- Host-only validators, synthetic tests, and a non-operational simulation.

There is currently no DroidXNU XNU patch set, Moto G60 XNU platform implementation, target build, XNU device driver, or device boot support.

## Testing model

Testing should progress from source and metadata validation to host-side tests. QEMU is a potential hardware-independent research category, as demonstrated by HakiOS, but no DroidXNU QEMU target or successful XNU execution has been established. Any future QEMU work must be separately scoped, documented, and evidenced.

No device access, firmware extraction, bootloader interaction, partition modification, flashing, or boot attempts are part of the current project scope.

## Reference

See [XNU architecture alignment](XNU_ARCHITECTURE_ALIGNMENT.md) for the comparison with HakiOS and the resulting DroidXNU design decisions.
