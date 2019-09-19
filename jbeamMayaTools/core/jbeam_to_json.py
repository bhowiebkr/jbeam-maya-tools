import os
import re
import json


def read(jbeam_file):
    """[summary]

    Args:
        fn (function): [description]


    """
    if not os.path.isfile(jbeam_file):
        print("file not found: {}".format(jbeam_file))
        return

    with open(jbeam_file, 'r') as f:
        j = f.read()

     # Comments
    j = re.sub(r'\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$',
               lambda m: m.group(1) or '', j, flags=re.MULTILINE)

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

    # add comma between numbers with spaces ie: 333 333 = 333, 333
    j = re.sub(r'(-?[0-9])\s+(-?[0-9])', r'\1,\2', j)

    # Add comma between number and "
    j = re.sub(r'([0-9])\s*("[a-zA-Z0-9_]*")', r'\1, \2', j)

    # missing comma between "bla""bla"
    j = re.sub(r'("[a-zA-Z0-9_]*")("[a-zA-Z0-9_]*")', r'\1, \2', j)

    # missing quotation on value in "bla": "bla
    j = re.sub(
        r'("[a-zA-Z0-9_]+"):(\s*"[a-zA-Z0-9_]+:)(\n\s*"[a-zA-Z]+")', r'\1:\2",\n\3', j)

    # missing comma after bool "bla":false"bla" = "bla":false, "bla"
    j = re.sub(r':(false|true)("[a-zA-Z_]+")', r':\1, \2', j)

    # edge case of missing comma inside of list
    j = re.sub(r'(["[a-zA-Z_0-9.?]+")\s(\["[a-zA-Z_]+"\]])', r'\1, \2', j)

    # missing number after decimal point
    j = re.sub(r'("[a-zA-Z0-9]+"):(-?[0-9])\.,\s?"', r'\1:\2.0,"', j)

    # remove junk at the end of file
    if j.endswith(','):
        j = j[:-1]

    # try to fix extra brackets at the end of file
    if not j.count('{') == j.count('}'):
        j = j[:-1]

    with open(r'C:\workarea\jbeam-maya-tools\temp\TEMP.json', 'w') as f:
        f.write(j)

    try:
        js = json.loads(j)
        return js
    except Exception:
        print(jbeam_file)
