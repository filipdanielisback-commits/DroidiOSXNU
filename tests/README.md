# Tests

Start with host-side checks that do not require a phone.

Run all synthetic tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

The test suite includes:

- Synthetic Device Tree parser fixtures. These are minimal examples, not copied from vendor source and do not assert Moto G60 hardware facts.
- Boot-flow simulator tests. These verify the simulator's reporting, injected-block behavior, and explicit non-bootable/no-hardware-access declarations. They do not test a real boot process.
- Platform profile validator tests. These check required fields, evidence metadata, unresolved hardware details, JSON error handling, and explicit host-only/non-bootable declarations. They validate structure, not physical hardware facts.

Future test reports should record:

- test name and purpose;
- exact source revision and tool versions;
- target device and verified hardware variant, if applicable;
- steps and expected result;
- observed result and relevant sanitized logs;
- known limitations.

Do not label a subsystem as working based only on a successful compile or a completed simulation.
