# XNU subsystem research map

**Pinned source:** Apple XNU `xnu-12377.121.6`  
**Pinned commit:** `ac9718fb1af618d5ce8678d0dc6e8a58f252216f`  
**Target profile:** Motorola Moto G60 (XT2135-2), research only

This map identifies real directories in the pinned upstream source and explains their conceptual relevance to DroidXNU. It is a reading and evidence map—not an implementation recipe, device configuration, or claim of hardware support.

## 1. Mach core — `osfmk/`

The upstream README identifies `osfmk/` as the Mach-based kernel subsystem area. Its pinned tree includes areas such as `osfmk/arm64/`, `osfmk/ipc/`, `osfmk/kern/`, `osfmk/vm/`, and `osfmk/mach/`.

| Source area | Research topic | DroidXNU question |
|---|---|---|
| `osfmk/arm64/` | ARM64-specific kernel implementation | Which parts are generic ARM64 architecture code, and which depend on Apple platform assumptions? |
| `osfmk/ipc/` | Mach IPC implementation | Which kernel abstractions are independent of the target board? |
| `osfmk/kern/` | Core kernel services | Which services depend on platform facilities that are not established for hanoip? |
| `osfmk/vm/` | Virtual memory subsystem | What platform memory-management contracts must be understood before any compatibility claim? |
| `osfmk/mach/` | Mach interfaces and definitions | Which interfaces form the common kernel contract? |

**Status:** upstream source areas confirmed. No DroidXNU Mach modifications or Moto G60 integration exist.

## 2. BSD layer — `bsd/`

The upstream README identifies `bsd/` as the BSD subsystem area. The pinned tree includes `bsd/kern/`, `bsd/vfs/`, `bsd/net/`, `bsd/netinet/`, `bsd/sys/`, and `bsd/security/`.

| Source area | Research topic | DroidXNU question |
|---|---|---|
| `bsd/kern/` | BSD process and kernel services | Which services rely on Mach interfaces or platform facilities? |
| `bsd/vfs/` | Virtual filesystem layer | What is part of the common kernel, and what depends on filesystem or storage drivers? |
| `bsd/net/`, `bsd/netinet/` | Networking protocols and interfaces | Keep protocol-stack code distinct from the missing hardware-facing radio support. |
| `bsd/sys/` | BSD system interfaces | Document the kernel/userspace boundary without assuming iOS userspace is available. |
| `bsd/security/` | BSD security-related code | Track policy and dependency boundaries; do not infer a complete iOS security environment. |

**Status:** upstream source areas confirmed. No Moto G60 filesystem, network, or security integration is implemented.

## 3. I/O Kit and driver framework — `iokit/` and `libkern/`

The pinned tree contains `iokit/IOKit/`, `iokit/Families/`, `iokit/Kernel/`, `iokit/DriverKit/`, and `libkern/`. The upstream README describes `libkern/` as including C++ IOKit library code for drivers and kernel extensions.

For this project, these are framework and interface research areas—not a promise that Android/Linux drivers can be reused or that every IOKit facility is available to an independent target.

Research questions:

- What abstractions does the public XNU driver framework expose?
- Which device responsibilities are handled by framework code versus platform-specific drivers?
- Which required Moto G60 devices have no evidenced XNU implementation?
- What source provenance and license review would be required before considering any external code?

**Status:** framework source exists upstream. DroidXNU has no Moto G60 IOKit driver implementation.

## 4. Platform Expert code — `pexpert/`

The upstream README describes `pexpert/` as containing platform-specific code, including interrupt handling and atomics. The pinned tree includes `pexpert/arm/` and `pexpert/pexpert/`.

This is a critical conceptual boundary: platform-specific kernel integration cannot be inferred from the presence of generic ARM64 code. DroidXNU must keep SoC-family clues separate from exact board facts and must leave unresolved hardware details explicitly unknown.

**Status:** upstream platform code exists. No hanoip-specific XNU platform layer has been demonstrated.

## 5. Startup and userspace boundary

The upstream README identifies `libsa/` as kernel bootstrap code and `libsyscall/` as the system-call library interface for userspace programs. These source areas are useful to understand XNU's wider architecture, but their presence does not establish a supported startup environment or a complete iOS system.

DroidXNU does not implement a target startup path, bootloader, installer, or iOS userspace. This project will not attempt device boot or modification as part of this research milestone.

## 6. Target mapping: what remains unknown

| Moto G60 subsystem | XNU research area | Current conclusion |
|---|---|---|
| CPU / ARM64 | `osfmk/arm64/`, `pexpert/arm/` | Architecture overlap only; platform integration unproven. |
| Memory management | `osfmk/vm/`, `osfmk/arm64/` | Required platform contracts not validated for the phone. |
| Interrupts and timers | `pexpert/`, `osfmk/arm64/` | Exact target integration not established. |
| Storage | `bsd/vfs/`, I/O Kit framework | No target XNU storage driver demonstrated. |
| Wi-Fi / Bluetooth | `bsd/net/`, I/O Kit framework | Android-side software clues do not establish XNU hardware support. |
| Display / touch | I/O Kit framework | No target XNU display or touch driver demonstrated. |
| Audio / camera / sensors / GPU | I/O Kit framework and platform layer | No target XNU drivers demonstrated. |

This table is a research index. It does not prescribe device operations and does not convert Android driver availability into XNU compatibility.

## 7. Evidence and provenance rules

Every future subsystem claim should record:

1. exact upstream repository, tag, and commit;
2. exact source path or document URL;
3. whether the statement is directly stated by the source or inferred;
4. confidence: confirmed, strong lead, unresolved, or unknown;
5. the exact device variant to which the claim applies;
6. any license or provenance review still required.

Do not mark a subsystem as supported because a directory exists, a generic interface is present, a file compiles, or another device uses a similarly named SoC.

## 8. References

- [Pinned XNU source tree](https://github.com/apple-oss-distributions/xnu/tree/xnu-12377.121.6)
- [Pinned upstream README](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/README.md)
- [Pinned ARM64 source directory](https://github.com/apple-oss-distributions/xnu/tree/xnu-12377.121.6/osfmk/arm64)
- [Pinned IOKit source directory](https://github.com/apple-oss-distributions/xnu/tree/xnu-12377.121.6/iokit)
- [DroidXNU ARM64 source architecture audit](XNU_ARM64_SOURCE_AUDIT.md)
- [Moto G60 XNU driver gap matrix](MOTO_G60_XNU_DRIVER_GAP_MATRIX.md)

---

**Result:** DroidXNU now has a source-backed reading map for the major XNU subsystem boundaries. This is research progress, not an operational kernel or phone port.
