import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
GUI = ROOT / "gui" / "boot-manager" / "index.html"
DOC = ROOT / "docs" / "BOOT_MANAGER_GUI.md"


class BootManagerGuiTests(unittest.TestCase):
    def test_gui_exists_and_declares_non_operational_scope(self):
        source = GUI.read_text(encoding="utf-8").lower()
        self.assertIn("simulation only", source)
        self.assertIn("non-bootable", source)
        self.assertIn("does not interact with a phone", source)
        self.assertIn("no hardware has been queried or changed", source)

    def test_interactions_are_limited_to_local_page_status(self):
        source = GUI.read_text(encoding="utf-8").lower()
        self.assertIn('addEventListener("click"', source)
        self.assertIn("log.textcontent", source)
        self.assertNotIn("fetch(", source)
        self.assertNotIn("xmlhttprequest", source)
        self.assertNotIn("webusb", source)
        self.assertNotIn("serialport", source)

    def test_documentation_states_no_device_operations(self):
        source = DOC.read_text(encoding="utf-8").lower()
        self.assertIn("does not communicate with android", source)
        self.assertIn("not a bootloader", source)
        self.assertIn("inert data-only", source)


if __name__ == "__main__":
    unittest.main()
