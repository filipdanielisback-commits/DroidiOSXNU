# Public XNU source baseline

This document pins a public XNU source snapshot for static research. It does not claim that XNU can boot on the Moto G60, and it does not authorize device experiments.

## Selected source revision

| Field | Value |
|---|---|
| Upstream repository | [apple-oss-distributions/xnu](https://github.com/apple-oss-distributions/xnu) |
| Release tag | `xnu-12377.121.6` |
| Annotated tag object | `9b6e7590204b89788e28b137ddfc897bb1292d8b` |
| Peeled commit | `ac9718fb1af618d5ce8678d0dc6e8a58f252216f` |
| Tag date | 2026-06-17 |
| Tag message | Imported from `xnu-12377.121.6.tar.gz` |
| Tag signature | Unsigned (GitHub reports `verified: false`) |
| Source license file | `APPLE_LICENSE` |
| License | Apple Public Source License 2.0 (APSL 2.0) |

The tag and commit were resolved through the upstream Git reference and annotated-tag objects. The tag is therefore recorded together with its peeled commit, rather than relying on a movable branch name. The tag is unsigned, so the tag metadata is not a cryptographic publisher signature.

- [Pinned source tree](https://github.com/apple-oss-distributions/xnu/tree/xnu-12377.121.6)
- [Pinned README](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/README.md)
- [Pinned APSL 2.0 text](https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/APPLE_LICENSE)
- [Tag object](https://api.github.com/repos/apple-oss-distributions/xnu/git/tags/9b6e7590204b89788e28b137ddfc897bb1292d8b)
- [Peeled commit](https://github.com/apple-oss-distributions/xnu/commit/ac9718fb1af618d5ce8678d0dc6e8a58f252216f)

## What this source establishes

The upstream README describes XNU as a hybrid kernel combining Mach, FreeBSD-derived components, and IOKit. It explicitly lists both `x86_64` and `ARM64` as supported architectures.

This is evidence that the public source contains ARM64 architecture support. It is **not** evidence that this XNU revision supports the Moto G60's specific SoC, board, boot chain, peripheral configuration, or Android firmware. Architecture support alone is not a platform port.

The public XNU repository is kernel source, not the complete iOS operating system. It does not provide all proprietary iOS userspace, platform drivers, firmware, signing assets, or other closed components.

## Upstream build-environment notes

The pinned README's external-developer guidance describes an Apple/macOS-oriented build environment:

- An Xcode version aligned with the macOS SDK being targeted.
- A matching Kernel Debug Kit (KDK) for Apple-silicon builds.
- Additional dependencies including AvailabilityVersions, libdispatch, and XNU headers; DTrace is described as optional.
- The documented build examples target Apple desktop platforms and their configurations.

These notes describe upstream requirements, not a validated DroidXNU build setup. No XNU build was attempted. No claim is made that Android, Termux, or a generic Linux host is a supported XNU build host for this project.

## License handling

The pinned source tree includes Apple's **Apple Public Source License 2.0** in `APPLE_LICENSE`. The license text and per-file notices must be reviewed before any source is copied, modified, redistributed, or externally deployed. APSL obligations can depend on what is distributed and how it is used; this document is not legal advice.

This pin does not change the license of DroidXNU as a whole. The repository has not selected a single project-wide license, and third-party components may have different terms. Do not remove Apple notices or assume that all files in the upstream repository have identical provenance.

## Research-only handling

- Do not vendor or mirror the XNU source tree in this repository as part of this milestone.
- Keep the upstream tag and commit identifiers as metadata.
- Do not fetch proprietary Apple or Motorola firmware, keys, signing materials, or private device data.
- Do not generate a bootable image, modify a phone, or change boot configuration as part of source-baseline work.
- Any future source-fetch tooling must verify the exact pinned commit and record integrity metadata before use.

## Evidence reviewed

- Upstream repository and README: https://github.com/apple-oss-distributions/xnu
- Pinned README: https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/README.md
- Pinned license: https://github.com/apple-oss-distributions/xnu/blob/xnu-12377.121.6/APPLE_LICENSE
- Pinned tag object and peeled commit: links above
