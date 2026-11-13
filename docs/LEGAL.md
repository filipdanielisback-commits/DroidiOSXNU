# Legal, firmware, and third-party policy

This document is project guidance, not legal advice.

## Public XNU source versus iOS

Apple publishes source for parts of its open-source operating-system components, including XNU. That does not make the complete iOS operating system open source. Proprietary frameworks, services, drivers, firmware, signing assets, and other components may not be available as source.

Do not describe an IPSW as source code. It is a firmware package containing compiled components and metadata.

## Pinned XNU source and license

The project records the public XNU snapshot `xnu-12377.121.6` and its peeled upstream commit in [the XNU source baseline](XNU_SOURCE_BASELINE.md). That snapshot includes Apple's Apple Public Source License 2.0 (`APPLE_LICENSE`). Review the actual license text and relevant per-file notices before copying, modifying, redistributing, or externally deploying any upstream source.

Recording this upstream license does not select a repository-wide DroidiOSXNU license and does not establish that every file in the upstream repository has identical provenance. Any third-party component may have different license terms.

## IPSW references

[IPSW.me](https://ipsw.me/) may be used as a firmware catalog/reference. This repository will not mirror firmware packages or redistribute extracted proprietary components. Do not add automated downloading, decryption, or security-circumvention workflows to this project.

The `ipsw/` directory is for documentation and safe metadata-oriented tooling only. Any local files supplied by a user must remain outside version control.

## Third-party code

Before importing code:

1. Identify the original project and exact revision.
2. Read its license and relevant notices.
3. Confirm that redistribution and modification are permitted.
4. Preserve copyright and license notices.
5. Record the component in a third-party inventory.

XNU-derived modifications must follow the applicable Apple Public Source License terms. Other components may have different licenses. Do not assume one repository-wide license automatically covers every dependency.

## Trademarks and affiliation

DroidiOSXNU is an independent research project. It is not affiliated with or endorsed by Apple, Motorola, Xiaomi, Google, or Qualcomm. Product and company names are used only to identify compatibility research targets.
