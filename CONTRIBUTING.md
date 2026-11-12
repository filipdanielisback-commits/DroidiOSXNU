# Contributing to DroidiOSXNU

Thanks for your interest. This project is in an early research phase, so careful documentation is as valuable as code.

## Before opening a change

1. Read [the project scope](README.md) and [legal policy](docs/LEGAL.md).
2. Check whether the topic already has an issue or research note.
3. Prefer small changes that can be reviewed and tested independently.
4. Identify the source and license of every third-party file or dependency.

## Research quality

For technical notes, label statements as one of:

- **Verified** — supported by a cited source, source inspection, or a reproducible test.
- **Hypothesis** — plausible but not yet demonstrated.
- **Unknown** — needs investigation.

Include device model, hardware revision where known, software version, commands or test procedure, and relevant logs with personal information removed.

## Code expectations

- Keep changes focused and readable.
- Do not add proprietary firmware, iOS binaries, keys, certificates, or private device dumps.
- Do not add code intended to bypass platform security, activation, or access controls.
- Preserve license headers and third-party notices.
- Add host-side tests for tools where practical.
- Never describe an untested feature as working.

## Pull requests

Explain the motivation, files changed, tests performed, and known limitations. For device-related changes, identify the exact device variant and distinguish tested hardware from assumed compatibility.

By contributing, you confirm that you have the right to submit the material under the terms that will apply to that contribution. A project-wide license decision is still pending.
