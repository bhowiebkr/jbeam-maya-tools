import os
import json


import pymel.all as pm

from jbeamMayaTools.core import common


def empty_vehicle(name):
    """Generate an empty vehicle
    """

    data = {}
    data[name] = {}
    data[name]['information'] = {}
    data[name]['information']['authors'] = 'bryan'
    data[name]['information']['name'] = name

    data[name]['slotType'] = 'main'

    # Nodes
    nodes = []
    nodes.append(["id", "posX", "posY", "posZ"])
    nodes.append({"nodeWeight": 10})
    nodes.append({"frictionCoef": 0.7})
    nodes.append({"nodeMaterial": "|NM_METAL"})
    nodes.append({"collision": True})
    nodes.append({"selfCollision": True})
    data[name]['nodes'] = nodes

    # Beams
    beams = []
    beams.append(["id1:", "id2:"])
    beams.append({"beamSpring": 2000000, "beamDamp": 200})
    beams.append({"beamDeform": 160000, "beamStrength": "800000"})
    data[name]['beams'] = beams

    # Camera
    data[name]['cameraExternal'] = {}
    data[name]['cameraExternal']['distance'] = 6.0
    data[name]['cameraExternal']['distanceMin'] = 4
    data[name]['cameraExternal']['offset'] = {'x': 0, "y": 0.0, 'z': 1.0}
    data[name]['cameraExternal']['fov'] = 65

    # Mesh
    data[name]['flexbodies'] = []
    data[name]['flexbodies'].append(['mesh', '[group]:', 'nonFlexMaterials'])
    data[name]['flexbodies'].append(['body', ['body']])

    # Ref Nodes
    data[name]['refNodes'] = []
    data[name]['refNodes'].append(["ref:", "back:", "left:", "up:"])
    data[name]['refNodes'].append(["ref0", "ref2", "ref1", "ref3"])

    return data


class Vehicle(object):
    def __init__(self, beam_vehicles_path, name, group):
        self.beam_vehicles_path = beam_vehicles_path
        self.name = name
        self.data = empty_vehicle(self.name)
        self.group = group

    def export(self):
        """General export method. jbeam, cs, mesh..
        """
        car_path = os.path.join(self.beam_vehicles_path, self.name)

        nodes = []

        nodes.append(['ref0', 0.0, 0.0, 0.0])
        nodes.append(['ref1', 0.2, 0.0, 0.0])
        nodes.append(['ref2', 0.0, 0.2, 0.0])
        nodes.append(['ref3', 0.0, 0.0, 0.2])

        nodes.append({'group': 'body'})

        beams = []

        for sub_group in self.group.listRelatives(type='transform'):
            if str(sub_group) == 'nodes_group':
                for node in sub_group.listRelatives(type='transform'):

                    nodes.append([str(node), float(node.tx.get())/100., float(
                        node.tz.get())/100., float(node.ty.get())/100.])
            elif str(sub_group) == 'beams_group':
                for beam in sub_group.listRelatives(type='transform'):
                    c = beam.getShape().listConnections(type='transform')

                    beams.append([str(c[0]), str(c[1])])

            elif str(sub_group) == 'mesh_group':
                # TODO publish mesh - rotate, freeze identity
                pass

        # Add the nodes to the data
        self.data[self.name]['nodes'].extend(nodes)
        self.data[self.name]['beams'].extend(beams)

        jbeam_path = os.path.join(car_path, self.name + '.jbeam')
        cs_path = os.path.join(car_path, 'name.cs')

        print('jbeam path: {}'.format(jbeam_path))
        print('cs path: {}'.format(cs_path))

        # jbeam (json)
        with open(jbeam_path, 'w') as outfile:
            outfile.write(json.dumps(self.data, indent=4, sort_keys=True))

        # CS file so the car shows in-game
        with open(cs_path, 'w') as f:
            f.write('%vehicleName = "{}";'.format(self.name))

        print('Export Done.')
