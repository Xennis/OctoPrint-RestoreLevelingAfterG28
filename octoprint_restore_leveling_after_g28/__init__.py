# coding=utf-8
from __future__ import absolute_import

import logging

import octoprint.plugin

class RestoreLevelingAfterG28Plugin():

	def rewrite_g28(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if not gcode or gcode != "G28":
			return

		cmd = [(cmd,), ("M420 S1",)]
		self._logger.info("Expand G28: {cmd}".format(**locals()))
		return cmd

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			restore_leveling_after_g28=dict(
				displayName="Restore Leveling After G28",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Xennis",
				repo="OctoPrint-RestoreLevelingAfterG28",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Xennis/OctoPrint-RestoreLevelingAfterG28/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Restore Leveling After G28"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = RestoreLevelingAfterG28Plugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.rewrite_g28,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
