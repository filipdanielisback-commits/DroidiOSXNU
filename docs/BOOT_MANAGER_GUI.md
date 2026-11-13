# Research GUI prototype

The repository contains browser-based visualizations for presenting research metadata. They are optional documentation aids, not part of the XNU kernel architecture.

## Scope

- Show the Moto G60 research profile and documented/unknown compatibility areas.
- Present clearly labeled simulated states for explaining project status.
- Run locally in a browser without a phone connection or external service.

## Non-operational boundary

The GUI is not a bootloader, installer, recovery environment, or iOS interface. It does not communicate with Android, a bootloader, USB devices, storage, partitions, firmware, or a kernel. Simulated progress is fictional and is not evidence of hardware compatibility.

The project direction is the actual public XNU kernel as a research foundation. UI work must not be presented as kernel implementation or allowed to distract from source analysis, platform research, and host-side validation.

Any future research image must remain **inert data-only** content; it must not contain executable boot code, a boot sector, partition table, filesystem, or device installation workflow.
