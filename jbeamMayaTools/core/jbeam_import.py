"""
each varient has a pc file

pc files maps meshes to jbeam files
"""
import json
import os
import glob
import re
import pymel.all as pm

vehicle_path = 'C:\\temp\\fullsize'


def convert_jbeam_to_json(jbeam_file):
    """[summary]

    Args:
        fn (function): [description]


    """
    if not os.path.isfile(jbeam_file):
        print("file not found: {}".format(jbeam_file))
        return

    j = ''

    with open(jbeam_file, 'r') as f:
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

    js = json.loads(j)

    return js


def dae_to_mb(dae_path, mb_path):
    """Convert a dae file to Maya binary

    Args:
        dae_path (str): Path to dae file
    """
    pm.newFile(force=True)
    pm.importFile(dae_path)

    name = os.path.basename(dae_path).split('.')[0]

    pm.select(pm.ls(type='mesh'))

    group = pm.group(world=True, name=name + '_group')

    for loc in pm.ls(type='locator'):
        pm.delete(loc.getParent())
    pm.saveAs(mb_path)


def import_mesh(dae_path):
    """Import mesh. cache it to a mb file if one doesn't exists.

    Args:
        dae_path (str): Path to dae file
    """
    ext = dae_path.split('.')[-1]
    mb_path = dae_path.replace('.' + ext, '.mb')
    if not os.path.exists(mb_path):
        dae_to_mb(dae_path=dae_path, mb_path=mb_path)

    name = os.path.basename(dae_path).split('.')[0]
    pm.importFile(mb_path)


def import_pc(pc_path):
    """Import pc file

    Args:
        pc_path (str): path to pc file

    Note:
        some of these pc files are invalid json files. Use a json linter online to find and fix these errors.
    """
    print(pc_path)

    data = None
    with open(pc_path, 'r') as f:
        data = json.load(f)

    print(data)


def import_jbeam(jbeam_path):
    print(jbeam_path)

    data = convert_jbeam_to_json(jbeam_file=jbeam_path)

    print(data)


def import_vehicle():
    """Import a vehicle
    """
    pm.newFile(force=True)
    print('importing: {}'.format(vehicle_path))

    print('\nImporting the dae files\n')

    # Import the mesh files
    for dae_path in glob.glob(os.path.join(vehicle_path, '*.dae')):
        import_mesh(dae_path=dae_path)

    print('\nImporting the pc files\n')

    # Import the pc files
    for pc_path in glob.glob(os.path.join(vehicle_path, '*.pc')):
        import_pc(pc_path=pc_path)

    print('\nImporting the jbeam files\n')

    # Import the pc files
    for jbeam_path in glob.glob(os.path.join(vehicle_path, '*.jbeam')):
        import_jbeam(jbeam_path=jbeam_path)
