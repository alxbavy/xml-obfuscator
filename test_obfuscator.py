import unittest
import os
import xml.etree.ElementTree as ET
from obfuscator import process_string, process_xml_file


class TestObfuscator(unittest.TestCase):

    def test_string_obfuscation(self):
        original = "Lokesh Gupta 111!"
        obfuscated = process_string(original, "obfuscate")

        self.assertNotEqual(original, obfuscated)
        self.assertEqual(len(original), len(obfuscated))
        self.assertTrue(obfuscated.endswith("!"))

        deobfuscated = process_string(obfuscated, "deobfuscate")
        self.assertEqual(original, deobfuscated)

    def test_xml_processing(self):
        test_xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <employees>
            <employee id="111">
                <firstName>Alex</firstName>
            </employee>
        </employees>"""

        with open("test_input.xml", "w", encoding="utf-8") as f:
            f.write(test_xml_content)

        process_xml_file("test_input.xml", "test_obfuscated.xml", "obfuscate")

        tree = ET.parse("test_obfuscated.xml")
        root = tree.getroot()
        employee = root.find("employee")
        self.assertNotEqual(employee.attrib["id"], "111")
        self.assertNotEqual(employee.find("firstName").text, "Alex")

        process_xml_file("test_obfuscated.xml", "test_deobfuscated.xml", "deobfuscate")

        tree_deobf = ET.parse("test_deobfuscated.xml")
        root_deobf = tree_deobf.getroot()
        employee_deobf = root_deobf.find("employee")
        self.assertEqual(employee_deobf.attrib["id"], "111")
        self.assertEqual(employee_deobf.find("firstName").text, "Alex")

        os.remove("test_input.xml")
        os.remove("test_obfuscated.xml")
        os.remove("test_deobfuscated.xml")


if __name__ == "__main__":
    unittest.main()