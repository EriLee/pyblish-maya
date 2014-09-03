from maya import cmds

import pyblish.backend.config


def collect_attributes(node, instance):
    """Store user-defined attributes from scene in instance `instance`

    Attributes:
        node (str): Maya node from which to collect attributes
        instance (Instance): Instance in which to store attributes

    """

    for attr in cmds.listAttr(node, userDefined=True):
        if attr == pyblish.backend.config.identifier:
            # Do not store the identifier itself
            continue

        try:
            instance.set_data(
                attr,
                value=cmds.getAttr(node + "." + attr))
        except:
            continue
