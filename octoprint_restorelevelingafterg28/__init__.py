# coding=utf-8
from __future__ import absolute_import

from octoprint.plugin import SettingsPlugin


class RestoreLevelingAfterG28Plugin(SettingsPlugin):

	ATCMD_RESTORE_LEVELING = "restore_leveling"

	def __init__(self):
		super(SettingsPlugin, self).__init__()
		self.leveling_enabled = False

	def hook_atcommand_sending(self, comm_instance, phase, command, parameters, tags=None, *args, **kwargs):
		if command != self.ATCMD_RESTORE_LEVELING:
			return
		if not self.leveling_enabled:
			self._logger.debug("Keep leveling disabled".format(**locals()))
			return

		cmd = "M420 S1"
		fade = self._settings.getFloat(["zFadeHeight"])
		if fade:
			cmd += " Z{fade}".format(fade=fade)
		self._logger.debug("Re-enable leveling: {cmd}".format(**locals()))
		self._printer.commands(cmd, tags=tags)

	def hook_gcode_queuing(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		if not gcode or gcode != "G28":
			return

		cmd = [
			("M420 V",),  # Current status
			(cmd, cmd_type, tags),
			("@{}".format(self.ATCMD_RESTORE_LEVELING),)  # Restore status
		]
		self._logger.debug("Expand G28: {cmd}".format(**locals()))
		return cmd

	def hook_gcode_received(self, comm_instance, line, *args, **kwargs):
		if not line or not line.startswith("echo:Bed Leveling"):
			return line

		self.leveling_enabled = bool("bed leveling on" in line.lower())
		self._logger.debug("Leveling is enabled: {self.leveling_enabled}".format(**locals()))
		return line

	##~~ Settings hook
	def get_settings_defaults(self):
		return dict(zFadeHeight=None)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			restorelevelingafterg28=dict(
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
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = RestoreLevelingAfterG28Plugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.atcommand.sending": __plugin_implementation__.hook_atcommand_sending,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.hook_gcode_queuing,
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.hook_gcode_received,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
