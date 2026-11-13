# Public XNU source versus a complete iOS system

## Purpose and scope

DroidXNU uses the pinned public XNU source as a kernel research baseline. **XNU source is not a complete iOS operating system.** A kernel source tree alone does not provide the full userspace, platform integration, trusted boot environment, or device-specific software needed to reproduce iOS.

This document records the boundary so that repository progress is not overstated. It is a static research note; it does not describe a procedure for assembling, installing, or booting an operating system.

## What the XNU repository provides

The pinned upstream tree (see [XNU source baseline](XNU_SOURCE_BASELINE.md)) contains the XNU kernel source. Its README describes a hybrid design incorporating Mach, FreeBSD-derived components, and IOKit, with ARM64 among its listed architectures.

That gives researchers material for studying kernel interfaces and implementation. It does not establish compatibility with the Moto G60's SoC, board wiring, boot firmware, peripherals, or Android software build.

## Major areas outside the XNU source tree

| Area | Why the kernel repository is not enough | DroidXNU status |
|---|---|---|
| User-space process environment | A running system needs user-space programs and libraries, not only a kernel. | No complete iOS-compatible userland is present or implemented. |
| System services and launch environment | Background services, service configuration, and system policy operate outside the kernel source tree. | Not present as an iOS service stack. |
| Frameworks and application APIs | iOS application frameworks and higher-level APIs are separate from XNU kernel interfaces. | Not implemented; no iOS app compatibility is claimed. |
| Device-specific drivers and support | Kernel architecture support does not supply drivers for a different vendor's board, display, radio, storage, sensors, or power management. | The Moto G60 driver-gap matrix records research leads and unresolved items; no device drivers are implemented. |
| Firmware and hardware support packages | Some platform components are separately distributed or proprietary and are not included in the public XNU repository. | Not collected, copied, or bundled by this project. |
| Boot trust and operating-system integrity | Apple's documented iPhone/iPad boot process relies on a chain of trusted, signed components; a kernel source checkout does not reproduce that trust environment. | No Apple boot chain, signing material, or device boot workflow is implemented. |
| Update, restore, and device-management infrastructure | A complete commercial operating system includes distribution, update, restore, and device-management systems beyond kernel code. | Outside this research project's current scope. |

The table describes categories and project boundaries, not a complete inventory of every iOS component or its licensing status.

## Open-source availability is component-specific

Apple publishes source releases and individual open-source projects. The existence of those releases is useful evidence that selected components are available for inspection; it does not mean that every component of iOS is published as one complete, reproducible source tree.

Each external component must be evaluated independently for:
- whether source code is actually published;
- the exact release/version and provenance;
- its license and file-level notices;
- dependencies and target-platform assumptions; and
- whether it is relevant to this kernel research project.

Do not assume that a component published for macOS or another Apple platform is automatically available, compatible, or licensed for use as an iOS replacement component.

## Security and platform boundary

Apple's public security documentation describes a verified boot chain for iPhone and iPad software, including signed boot components and the kernel. It also describes runtime protections such as app sandboxing, entitlements, and code-signing restrictions.

These are system-level properties, not features supplied by the XNU source tree alone. This project does not attempt to reproduce Apple's signing infrastructure, obtain private signing assets, bypass security controls, or modify a device.

## Consequences for project claims

The following statements are accurate:

- The project studies a pinned public XNU kernel revision.
- The selected upstream source lists ARM64 support.
- The Moto G60 research profile and driver-gap matrix document known facts, source leads, and unresolved hardware questions.
- Host-side validators and simulations test documentation and metadata only.

The following statements are **not** supported:

- "iOS is open source."
- "The XNU repository contains the complete iOS operating system."
- "ARM64 support means XNU supports the Moto G60."
- "A successful host-side test means the phone can boot or run iOS."
- "DroidXNU has iOS userspace, working hardware drivers, or a bootable image."

## Project handling rules

- Keep the work focused on static source research, documentation, and host-only tests.
- Do not copy proprietary firmware, private signing assets, vendor blobs, or personal device data into the repository.
- Review the exact license and notices for every separately published source component before considering reuse.
- Keep unknown platform and hardware details explicitly marked as unknown.
- Do not treat simulations, source inspection, or metadata validation as device tests.

## References

- [Pinned XNU source baseline](XNU_SOURCE_BASELINE.md)
- [Apple XNU source repository](https://github.com/apple-oss-distributions/xnu)
- [Apple Open Source releases](https://opensource.apple.com/releases/)
- [Apple Open Source projects](https://opensource.apple.com/projects/)
- [Apple Platform Security: Boot process for iPhone and iPad](https://support.apple.com/guide/security/boot-process-for-iphone-and-ipad-devices-secb3000f149/web)
- [Apple Platform Security: Runtime process security](https://support.apple.com/guide/security/security-of-runtime-process-sec15bfe098e/web)
