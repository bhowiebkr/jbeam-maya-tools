import pymel.all as pm


def lock_hide(o):
    """Lock and hide transform attributes on the object
    """
    for each in ['t', 'r', 's']:
        for ax in ['x', 'y', 'z']:
            o.attr(each + ax).set(lock=True, keyable=False, channelBox=False)
    o.v.set(lock=True, keyable=False, channelBox=False)


def make_groups(car_name):
    """Helper - Make common groups
    """
    group = pm.group(name=car_name + '_group', empty=True)
    nodes_group = pm.group(name='nodes_group', empty=True, parent=group)
    beams_group = pm.group(name='beams_group', empty=True, parent=group)
    return group, nodes_group, beams_group


def make_node(name, parent, vtx):
    """Make a Node from a vertex location
    """
    loc = pm.spaceLocator()
    loc.rename(name)
    loc.t.set(vtx.getPosition(space='world'))
    loc.overrideEnabled.set(True)
    loc.overrideColor.set(17)
    loc.setParent(parent)


def make_beam(index, c, group):
    """Make a beam from 2 Nodes
    """
    curve = pm.curve(p=[(0, 0, 0), (1, 0, 0)], degree=1)
    curve.rename('beam_' + str(index))
    shape = curve.getShape()
    curve.overrideEnabled.set(True)
    curve.overrideColor.set(15)
    lock_hide(curve)

    start = pm.DependNode('b' + str(c[0]))
    end = pm.DependNode('b' + str(c[1]))

    start.t >> shape.controlPoints[0]
    end.t >> shape.controlPoints[1]
    curve.setParent(group)
    index += 1


def build_truss(car_name):
    """Method 2 - This builder makes a truss like structure
    """
    sel = pm.ls(sl=True)
    if not sel:
        return

    group, nodes_group, beams_group = make_groups(car_name=car_name)

    mesh = sel[0].getShape()

    # Organize the connections
    connections = []
    verts = mesh.verts
    for index, vtx in enumerate(verts):

        # Make the locators
        make_node(name='b' + str(index), parent=nodes_group,
                  vtx=vtx)

        vert_list = []
        for face in vtx.connectedFaces():
            for v in face.getVertices():
                vert_list.append(v)
        vert_list = list(set(vert_list))
        vert_list.remove(index)

        print('vtx: {} connected: {}'.format(index, str(vert_list)))

        for v in vert_list:
            c = sorted([index, v])
            if c not in connections:
                connections.append(c)
                print('\tadding: {}'.format(c))

    # Make the connections
    for i, c in enumerate(connections):
        make_beam(index=i, c=c, group=beams_group)


def build_box(car_name):
    """Method 1 - This buider make box strucutre (not strong)
    """
    sel = pm.ls(sl=True)

    group = pm.group(name=car_name + '_group', empty=True)
    nodes_group = pm.group(name='nodes_group', empty=True, parent=group)
    beams_group = pm.group(name='beams_group', empty=True, parent=group)

    if not sel:
        return

    trans = sel[0]
    mesh = trans.getShape()
    pm.hide(trans)

    d = {}
    verts = mesh.verts
    for index, vtx in enumerate(verts):

        loc = pm.spaceLocator()
        loc.rename('b' + str(index))
        loc.t.set(vtx.getPosition(space='world'))
        loc.overrideEnabled.set(True)
        loc.overrideColor.set(17)
        loc.setParent(nodes_group)

        index = vtx.index()
        d[index] = {'loc': loc, 'connected': []}

        for c in vtx.connectedVertices():
            c_index = c.index()
            if c_index < index:
                continue
            d[index]['connected'].append(c_index)

    index = 0
    for each in d:
        loc = d[each]['loc']

        for other in d[each]['connected']:
            other_loc = d[other]['loc']

            curve = pm.curve(p=[(0, 0, 0), (1, 0, 0)], degree=1)
            curve.rename('beam_' + str(index))
            shape = curve.getShape()
            curve.overrideEnabled.set(True)
            curve.overrideColor.set(15)
            lock_hide(curve)
            loc.t >> shape.controlPoints[0]
            other_loc.t >> shape.controlPoints[1]
            curve.setParent(beams_group)
            index += 1

    pm.select(clear=True)
