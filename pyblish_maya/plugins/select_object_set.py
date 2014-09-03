import pyblish.backend.lib
import pyblish.backend.config
import pyblish.backend.plugin

# Local library
import pyblish_maya.lib

# Host library
import maya.cmds as cmds


@pyblish.backend.lib.log
class SelectObjectSet(pyblish.backend.plugin.Selector):
    """Select instances of node-type 'transform'

    Opens up the doors for instances containing nodes of any type,
    but lacks the ability to be nested with DAG nodes.

    E.g.          -> /root/MyCharacter.publishable/an_object_set

    """

    hosts = ['maya']
    version = (0, 1, 0)

    def process_context(self, context):
        for objset in cmds.ls("*." + pyblish.backend.config.identifier,
                              recursive=True,
                              objectsOnly=True,
                              type='objectSet'):

            instance = context.create_instance(name=objset)

            for node in cmds.sets(objset, query=True):
                if cmds.nodeType(node) == 'transform':
                    descendents = cmds.listRelatives(node,
                                                     allDescendents=True)
                    for descendent in descendents:
                        instance.add(descendent)

                instance.add(node)

            pyblish_maya.lib.collect_attributes(node=objset, instance=instance)
