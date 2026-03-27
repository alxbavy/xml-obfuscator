import xml.etree.ElementTree as ET
import argparse
import sys

SOURCE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
TARGET = "Q5A8ZWS0XEDC6RFVT9GBY4HNU3J2MI1KO7LPqazwsxedcrfvtgbyhnujmikolp"


def process_string(text: str, mode: str) -> str:
    """
    Обфусцирует или деобфусцирует строку на основе таблицы подстановок.
    Символы, которых нет в SOURCE/TARGET (например, пробелы, знаки препинания), остаются без изменений.
    """
    if not text:
        return text

    if mode == "obfuscate":
        trans = str.maketrans(SOURCE, TARGET)
    elif mode == "deobfuscate":
        trans = str.maketrans(TARGET, SOURCE)
    else:
        raise ValueError("Unknown mode. Use 'obfuscate' or 'deobfuscate'.")

    return text.translate(trans)


def process_xml_file(input_path: str, output_path: str, mode: str):
    """
    Читает XML, рекурсивно обходит все узлы, изменяет текст и атрибуты, сохраняет результат.
    """
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()

        for elem in root.iter():
            if elem.text:
                elem.text = process_string(elem.text, mode)

            if elem.tail:
                elem.tail = process_string(elem.tail, mode)

            for attr_name, attr_value in elem.attrib.items():
                elem.attrib[attr_name] = process_string(attr_value, mode)

        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Success! File saved to: {output_path}")

    except Exception as e:
        print(f"Error processing XML: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="XML Data Obfuscator/Deobfuscator")
    parser.add_argument("mode", choices=["obfuscate", "deobfuscate"], help="Operation mode")
    parser.add_argument("-i", "--input", required=True, help="Path to input XML file")
    parser.add_argument("-o", "--output", required=True, help="Path to output XML file")

    args = parser.parse_args()
    process_xml_file(args.input, args.output, args.mode)


if __name__ == "__main__":
    main()