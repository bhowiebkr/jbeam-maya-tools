"""
each varient has a pc file

pc files maps meshes to jbeam files
"""
import json
import os
import glob
import re
import pymel.all as pm

from jbeamMayaTools.core import jbeam_to_json
from jbeamMayaTools.core import maya_builders

vehicle_path = r'C:\temp\vehicles\etk800\vehicles\etk800'


def dae_to_mb(dae_path, mb_path):
    """Convert a dae file to Maya binary

    Args:
        dae_path (str): Path to dae file
    """
    pm.newFile(force=True)
    pm.importFile(dae_path)

    name = os.path.basename(dae_path).split('.')[0]

    pm.select(pm.ls(type='mesh'))

    group = pm.group(world=True, name=name + '_meshGroup')

    for loc in pm.ls(type='locator'):
        pm.delete(loc.getParent())
    pm.saveAs(mb_path)


def import_mesh(vehicle_path):
    """Import mesh. cache it to a mb file if one doesn't exists.

    Args:
        dae_path (str): Path to dae file
    """

    pm.newFile(force=True)

    mb_paths = []

    for dae_path in glob.glob(os.path.join(vehicle_path, '*.dae')):
        # import_mesh(dae_path=dae_path)

        ext = dae_path.split('.')[-1]
        mb_path = dae_path.replace('.' + ext, '.mb')
        if not os.path.exists(mb_path):
            dae_to_mb(dae_path=dae_path, mb_path=mb_path)

        mb_paths.append(mb_path)

        # name = os.path.basename(dae_path).split('.')[0]

    pm.newFile(force=True)

    for f in mb_paths:
        pm.importFile(f)

    # Cleanup

    # Remove lights
    for light in pm.ls(type='pointLight'):
        pm.delete(light.getParent())

    # Group mesh
    root_grp = pm.group(empty=True, world=True, name='mesh')
    for grp in pm.ls(assemblies=True):
        if grp != root_grp and not grp.getShape():
            grp.setParent(root_grp)


def import_pc(pc_path):
    """Import pc file

    Args:
        pc_path (str): path to pc file

    Note:
        some of these pc files are invalid json files. Use a json linter online to find and fix these errors.
    """
    print(pc_path)

    # data = None
    # with open(pc_path, 'r') as f:
    #     data = json.load(f)

    # print(data)


def import_jbeam_nodes(root, jbeam_path):

    print('importing jbeam nodes: {}'.format(jbeam_path))
    data = jbeam_to_json.read(jbeam_file=jbeam_path)
    print('data: {}'.format(data))

    if not data:
        return

    jbean_grp_name = os.path.basename(jbeam_path).split('.')[0] + '_group'
    jbeam_grp = pm.group(empty=True, parent=root, name=jbean_grp_name)

    for root in data.keys():
        # print('\t{}'.format(root))

        root_grp = pm.group(empty=True, parent=jbeam_grp, name=root + '_group')
        nodes_grp = pm.group(empty=True, parent=root_grp, name='nodes')

        nodes = []
        beams = []

        # Build nodes
        for key in data[root].keys():
            # print('\t\t{}'.format(key))
            if key == 'nodes':
                for node_val in data[root]['nodes']:

                    if not type(node_val) == list:
                        # read settings here
                        continue

                    if node_val[1] == 'posX':
                        continue

                    # simple nodes
                    if len(node_val) == 4:
                        # print('\t\t\t{}'.format(node_val))
                        point = [node_val[1], node_val[2], node_val[3]]
                        # print('point: {}'.format(point))

                        maya_builders.make_node(
                            name=node_val[0], parent=nodes_grp, point=point)

                    # complex nodes
                    else:
                        pass


def import_jbeam_beams(root, jbeam_path):

    # Build Beams
    data = jbeam_to_json.read(jbeam_file=jbeam_path)

    if not data:
        return

    jbean_grp_name = os.path.basename(jbeam_path).split('.')[0]

    b_index = 0

    for root in data.keys():

        root_grp_name = 'jbeam|{}_group|{}_group'.format(jbean_grp_name, root)

        root_grp = pm.DependNode(root_grp_name)
        # print('root_grp: {}'.format(root_grp))
        beams_grp = pm.group(empty=True, parent=root_grp, name='beams')
        for key in data[root].keys():
            if key == 'beams':
                for beam_val in data[root]['beams']:

                    if not type(beam_val) == list:
                        # read settings here
                        continue

                    if len(beam_val) == 2 and beam_val[0] == 'id1:':
                        continue

                    # print('\t\t\t{}'.format(beam_val))

                    # Create the beam

                    if pm.objExists(beam_val[0]) and pm.objExists(beam_val[1]):
                        # print('making beam with: {} and {}'.format(
                        #     beam_val[0], beam_val[1]))
                        maya_builders.make_beam(
                            index=b_index, c=beam_val, group=beams_grp)

                        b_index += 1


def import_vehicle():
    """Import a vehicle
    """
    pm.newFile(force=True)
    print('importing: {}'.format(vehicle_path))

    print('\nImporting the dae files\n')

    # Import the mesh files

    import_mesh(vehicle_path=vehicle_path)

    print('\nImporting the pc files\n')

    # Import the pc files
    for pc_path in glob.glob(os.path.join(vehicle_path, '*.pc')):
        import_pc(pc_path=pc_path)

    print('\nImporting the jbeam files\n')

    # Import the jbeam files
    grp = pm.group(empty=True, world=True, name='jbeam')

    # Import nodes first
    for jbeam_path in glob.glob(os.path.join(vehicle_path, '*.jbeam')):
        import_jbeam_nodes(root=grp, jbeam_path=jbeam_path)

    # Import beams
    for jbeam_path in glob.glob(os.path.join(vehicle_path, '*.jbeam')):
        import_jbeam_beams(root=grp, jbeam_path=jbeam_path)
