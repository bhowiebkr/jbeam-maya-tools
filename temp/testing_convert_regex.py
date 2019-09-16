import re
import sys
import os
import json
import glob


def main():

    vehicle_path = 'C:\\temp\\all_jbeam'

    invalid_files = 0
    converted = 0

    # Import the pc files
    i = 0
    total = len(glob.glob(os.path.join(vehicle_path, '*.jbeam')))
    for jbeam_path in glob.glob(os.path.join(vehicle_path, '*.jbeam')):

        # print('current:', jbeam_path, i)

        with open(jbeam_path, 'r') as f:
            j = f.read()

        # single line comments
        j = re.sub(r'\/\/.*', r'', j)

        # multiline comments
        j = re.sub(r'/\*[\s\S]*?\*/', '', j)

        # Missing comma between brackets
        j = re.sub(r'(\]|})\s*?(\{|\[)', r'\1,\2', j)

        # Add expected comma between } or ] and "
        j = re.sub(r'(}|])\s*"', r'\1,"', j)

        # Adding expected comma between " and {
        j = re.sub(r'"{', r'", {', j)

        j = re.sub(r'"\s+("|\{)', r'",\1', j)

        # add comma between bool keys
        j = re.sub(r'(false|true)\s+"', r'\1,"', j)

        # remove doubled comma's
        j = re.sub(r',\s*,', r',', j)

        # add comma between numbers and numbers or [
        j = re.sub(r'("[a-zA-Z0-9_]*")\s(\[|[0-9])', r'\1, \2', j)

        # Add a comma between number and {
        j = re.sub(r'(\d\.*\d*)\s*{', r'\1, {', j)

        j = re.sub(r'([0-9]\n)', r'\1,', j)

        # Remove trailing comma
        j = re.sub(r',\s*?(]|})', r'\1', j)

        # single line comments
        j = re.sub(r'\/\/.*', r'', j)

        # add comma between numbers with spaces ie: 333 333 = 333, 333
        j = re.sub(r'([0-9])\s+([0-9])', r'\1,\2', j)

        # Add comma between number and "
        j = re.sub(r'([0-9])\s*("[a-zA-Z0-9_]*")', r'\1, \2', j)

        # missing comma between "bla""bla"
        j = re.sub(r'("[a-zA-Z0-9_]*")("[a-zA-Z0-9_]*")', r'\1, \2', j)

        # missing quotation on value in "bla": "bla
        j = re.sub(
            r'("[a-zA-Z0-9_]+"):(\s*"[a-zA-Z0-9_]+:)(\n\s*"[a-zA-Z]+")', r'\1:\2",\n\3', j)

        with open('temp\\TEMP.json', 'w') as f:
            f.write(j)

        try:
            test = json.loads(j)
            converted += 1

        except Exception as e:
            print('\n', e, '\n', jbeam_path,
                  '\n\n{}/{}'.format(i, total))
            invalid_files += 1

        i += 1

    print('total: {}, converted: {}, invalid: {}'.format(
        total, converted, invalid_files))


if __name__ == '__main__':
    main()
