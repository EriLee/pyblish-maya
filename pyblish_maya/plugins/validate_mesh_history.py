import pyblish.backend.plugin

import pymel.core as pm


class ValidateMeshHistory(pyblish.backend.plugin.Validator):
    """Check meshes for construction history"""

    families = ['model']
    hosts = ['maya']
    version = (0, 1, 0)

    def process(self, context):
        for instance in pyblish.backend.plugin.instances_by_plugin(
                instances=context, plugin=self):

            try:
                for node in instance:
                    node = pm.PyNode(node)

                    try:
                        if node.inMesh.listConnections():
                            raise ValueError(
                                'Construction History on: %s' % node)
                    except AttributeError:
                        # node is not a mesh
                        pass

            except ValueError as exc:
                yield instance, exc

            else:
                # Everything went well
                yield instance, None

    def fix(self, context):
        for instance in self.instances(context):
            for node in instance:
                node = pm.PyNode(node)
                pm.delete(node, ch=True)
