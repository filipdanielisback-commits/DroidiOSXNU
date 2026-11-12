# Tests

Start with host-side checks that do not require a phone.

Run the synthetic Device Tree parser tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

The DTS fixtures in these tests are minimal, synthetic examples; they are not copied from vendor source and do not assert Moto G60 hardware facts.

Future test reports should record:

- test name and purpose;
- exact source revision and tool versions;
- target device and verified hardware variant, if applicable;
- steps and expected result;
- observed result and relevant sanitized logs;
- known limitations.

Do not label a subsystem as working based only on a successful compile.
