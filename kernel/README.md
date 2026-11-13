# Kernel research

This directory contains DroidiOSXNU's XNU source pin, original integration notes, and future project-owned patches.

## Upstream source

The project pins Apple's public XNU repository to `xnu-12377.121.6`, commit `ac9718fb1af618d5ce8678d0dc6e8a58f252216f`. The pin and Apple Public Source License 2.0 metadata are recorded in [xnu-source-pin.json](xnu-source-pin.json).

Fetch the exact upstream source into a separate local working tree:

```sh
python tools/fetch_xnu_source.py
```

The tool checks the annotated tag object and peeled commit before checking out a detached HEAD at the pinned commit. The default destination is `kernel/upstream/xnu`, which is ignored by Git so Apple's source is not silently copied into this project repository. The checkout retains upstream license and copyright notices.

The fetcher refuses to overwrite a dirty working tree, a non-Git destination, or a repository with a different origin. It requires Git and network access. It does not build XNU or access a device.

## Source and change separation

- Apple's upstream tree is the source of truth for unmodified XNU code.
- DroidiOSXNU-owned research and changes belong outside the ignored upstream checkout.
- Any future patch must identify the exact upstream file and commit, explain the change, and preserve required Apple notices.
- Do not import third-party driver code without a separate provenance and license review.

See [XNU ARM64 platform foundations](../docs/XNU_ARM64_PLATFORM_FOUNDATIONS.md) for the initial source review map.

## Current status

The source pin, fetcher, and host-side tests are committed. The local source checkout has not yet been run or independently reviewed in this environment. No Moto G60 platform code, target build, driver, or hardware support is claimed.
