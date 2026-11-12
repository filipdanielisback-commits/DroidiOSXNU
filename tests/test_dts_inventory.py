import unittest

from tools.dts_inventory import parse_dts


class DtsInventoryTests(unittest.TestCase):
    def test_extracts_nested_nodes_and_selected_properties(self):
        source = '''
/dts-v1/;
/ {
    soc {
        uart@1000 {
            compatible = "acme,uart-v2", "acme,uart";
            reg = <0x1000 0x100>;
            status = "okay";
        };
        disabled-device@2000 {
            compatible = "acme,unused";
            status = "disabled";
        };
    };
};
'''
        rows = parse_dts(source, "fixture.dts")
        self.assertEqual(len(rows), 2)
        uart = next(row for row in rows if row["path"].endswith("uart@1000"))
        self.assertEqual(uart["compatible"], '"acme,uart-v2" , "acme,uart"')
        self.assertEqual(uart["reg"], "<0x1000 0x100>")
        self.assertEqual(uart["status"], '"okay"')
        disabled = next(row for row in rows if row["path"].endswith("disabled-device@2000"))
        self.assertEqual(disabled["status"], '"disabled"')

    def test_ignores_comments_and_braces_inside_strings(self):
        source = '''
/ {
    /* compatible = "wrong,comment"; */
    device@0 {
        compatible = "vendor,brace-{device}"; // status = "disabled";
    };
};
'''
        rows = parse_dts(source)
        self.assertEqual(len(rows), 1)
        self.assertIn("brace-{device}", rows[0]["compatible"])

    def test_records_overlay_fragment(self):
        source = '&uart0 { status = "okay"; };'
        rows = parse_dts(source, "overlay.dtsi")
        self.assertEqual(rows[0]["path"], "/&uart0")
        self.assertEqual(rows[0]["status"], '"okay"')

    def test_nodes_without_tracked_properties_are_omitted(self):
        self.assertEqual(parse_dts("/ { chosen { bootargs = \"quiet\"; }; };"), [])


if __name__ == "__main__":
    unittest.main()
