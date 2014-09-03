import pyblish.backend.plugin

from maya import cmds


class ValidateReviewInstances(pyblish.backend.plugin.Validator):
    """If there are any review instances, validate them

    Ensure that review selections contain a camera.

    """

    families = ['review']
    hosts = ['maya']

    def process_instance(self, instance):
        cameras = cmds.ls(type='camera')
        for camera in cameras:
            if camera in instance:
                return

        raise ValueError("No camera found in instance: {0}".format(instance))
