import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOBILE = ROOT / "gui" / "boot-manager" / "mobile.html"


class MobileBootManagerGuiTests(unittest.TestCase):
    def test_mobile_layout_and_sections_exist(self):
        source = MOBILE.read_text(encoding="utf-8").lower()
        self.assertIn('name="viewport"', source)
        self.assertIn("mobile-first", source)
        self.assertIn('data-tab="overview"', source)
        self.assertIn('data-tab="platform"', source)
        self.assertIn('data-tab="about"', source)
        self.assertIn("@media(max-width:360px)", source)

    def test_simulation_is_non_operational(self):
        source = MOBILE.read_text(encoding="utf-8").lower()
        self.assertIn("simulation only", source)
        self.assertIn("not a bootloader", source)
        self.assertIn("does not interact with a phone", source)
        self.assertIn("no device access", source)
        self.assertNotIn("fetch(", source)
        self.assertNotIn("xmlhttprequest", source)
        self.assertNotIn("webusb", source)
        self.assertNotIn("serialport", source)


if __name__ == "__main__":
    unittest.main()
