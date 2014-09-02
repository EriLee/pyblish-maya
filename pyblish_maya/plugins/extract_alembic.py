import os
import tempfile

import pyblish.backend.lib
import pyblish.backend.plugin

from maya import cmds
import maya.mel as mel


@pyblish.backend.lib.log
class ExtractAlembic(pyblish.backend.plugin.Extractor):
    """Extract family members to Alembic format

    Attributes:
        families: The extractor is triggered upon families of "model"
        hosts: This extractor is designed for Autodesk Maya
        version: The current version of the extractor.

    """

    families = ['model']
    hosts = ['maya']
    version = (0, 1, 0)

    def process(self, context):
        cmds.loadPlugin('AbcExport.mll', quiet=True)
        cmds.loadPlugin('AbcImport.mll', quiet=True)

        #get time range
        start = cmds.playbackOptions(q=True, animationStartTime=True)
        end = cmds.playbackOptions(q=True, animationEndTime=True)

        for instance in pyblish.backend.plugin.instances_by_plugin(
                instances=context, plugin=self):
            # Note: Did you really mean to extract each node
            # as an alembic individually, and not the entire
            # collection of nodes?
            for node in instance:
                temp_dir = tempfile.mkdtemp()
                temp_file = os.path.join(temp_dir, '{0}.abc'.format(
                    node.replace(':', '-')))

                self.log.info("Extracting locally..")
                previous_selection = cmds.ls(selection=True)
                cmd = ' -root ' + node
                mel_cmd = 'AbcExport -j \"-frameRange {start} {end} '.format(
                    start=start, end=end)
                mel_cmd += '-writeVisibility -uvWrite -worldSpace '
                mel_cmd += '{cmd} -file'.format(cmd=cmd)
                mel_cmd += ' \\\"%s\\\"\";' % temp_file.replace('\\', '/')
                mel.eval(mel_cmd)

                # This needs to happen per instance, not per node
                # self.commit(path=temp_dir, instance=instance)

                if previous_selection:
                    cmds.select(previous_selection, replace=True)
                else:
                    cmds.select(deselect=True)

                self.log.info("Extraction successful.")

            yield instance, None  # Value, Exception
