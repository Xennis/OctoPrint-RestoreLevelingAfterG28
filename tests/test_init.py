import unittest

from mock import Mock, MagicMock
from octoprint.settings import Settings

from octoprint_restorelevelingafterg28 import RestoreLevelingAfterG28Plugin


class TestHookAtcommandSending(unittest.TestCase):

	def test_cmd_none(self):
		cmd = None
		p = RestoreLevelingAfterG28Plugin()
		p._logger = MagicMock()
		actual = p.hook_atcommand_sending(None, None, cmd, None)
		self.assertIsNone(actual)

	def test_some_cmd(self):
		cmd = "some_cmd"
		p = RestoreLevelingAfterG28Plugin()
		p._logger = MagicMock()
		actual = p.hook_atcommand_sending(None, None, cmd, None)
		self.assertIsNone(actual)

	def test_cmd_leveling_off(self):
		cmd = "restore_leveling"
		p = RestoreLevelingAfterG28Plugin()
		p._logger = MagicMock()
		actual = p.hook_atcommand_sending(None, None, cmd, None)
		self.assertIsNone(actual)
		p._logger.debug.assert_called_once_with("Keep leveling disabled")

	def test_cmd_leveling_on(self):
		cmd = "restore_leveling"
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		p._printer = MagicMock()
		p._settings = MagicMock()
		p._settings.getFloat = Mock(return_value=None)
		actual = p.hook_atcommand_sending(None, None, cmd, None, tags=["tag1", "tag2"])
		self.assertIsNone(actual)
		p._logger.debug.assert_called_once_with("Re-enable leveling: M420 S1")
		p._printer.commands.assert_called_once_with("M420 S1", tags=["tag1", "tag2"])
		p._settings.getFloat.assert_called_once_with(["zFadeHeight"])

	def test_cmd_leveling_on_tags_none(self):
		cmd = "restore_leveling"
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		p._printer = MagicMock()
		p._settings = MagicMock()
		p._settings.getFloat = Mock(return_value=None)
		actual = p.hook_atcommand_sending(None, None, cmd, None, tags=None)
		self.assertIsNone(actual)
		p._logger.debug.assert_called_once_with("Re-enable leveling: M420 S1")
		p._printer.commands.assert_called_once_with("M420 S1", tags=None)
		p._settings.getFloat.assert_called_once_with(["zFadeHeight"])

	def test_cmd_leveling_on_with_fade(self):
		cmd = "restore_leveling"
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		p._printer = MagicMock()
		p._settings = MagicMock()
		p._settings.getFloat = Mock(return_value=2.0)
		actual = p.hook_atcommand_sending(None, None, cmd, None, tags=None)
		self.assertIsNone(actual)
		p._logger.debug.assert_called_once_with("Re-enable leveling: M420 S1 Z2.0")
		p._printer.commands.assert_called_once_with("M420 S1 Z2.0", tags=None)
		p._settings.getFloat.assert_called_once_with(["zFadeHeight"])

	def test_cmd_leveling_on_with_fade_zero(self):
		cmd = "restore_leveling"
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		p._printer = MagicMock()
		p._settings = MagicMock()
		p._settings.getFloat = Mock(return_value=0)
		actual = p.hook_atcommand_sending(None, None, cmd, None, tags=None)
		self.assertIsNone(actual)
		p._logger.debug.assert_called_once_with("Re-enable leveling: M420 S1")
		p._printer.commands.assert_called_once_with("M420 S1", tags=None)
		p._settings.getFloat.assert_called_once_with(["zFadeHeight"])


class TestHookQueuing(unittest.TestCase):

	def test_none(self):
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		actual = p.hook_gcode_queuing(None, None, cmd=None, cmd_type=None, gcode=None)
		self.assertIsNone(actual)

	def test_some_cmd(self):
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		actual = p.hook_gcode_queuing(None, None, cmd="G30", cmd_type=None, gcode="G30")
		self.assertIsNone(actual)

	def test_expand(self):
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		actual = p.hook_gcode_queuing(None, None, cmd="G28 X Z", cmd_type="type1", gcode="G28", tags=["tag1", "tag2"])
		expected = [
			("M420 V",),
			("G28 X Z", "type1", ["tag1", "tag2"]),
			("@restore_leveling",)
		]
		self.assertEqual(expected, actual, msg="cmd")
		p._logger.debug.assert_called_once_with("Expand G28: {}".format(expected))

	def test_expand_no_type_and_no_tags(self):
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		actual = p.hook_gcode_queuing(None, None, cmd="G28 X Z", cmd_type=None, gcode="G28", tags=None)
		expected = [
			("M420 V",),
			("G28 X Z", None, None),
			("@restore_leveling",)
		]
		self.assertEqual(expected, actual, msg="cmd")
		p._logger.debug.assert_called_once_with("Expand G28: {}".format(expected))

	def test_expand_no_parameters(self):
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		actual = p.hook_gcode_queuing(None, None, cmd="G28", cmd_type=None, gcode="G28", tags=None)
		expected = [
			("M420 V",),
			("G28", None, None),
			("@restore_leveling",)
		]
		self.assertEqual(expected, actual, msg="cmd")
		p._logger.debug.assert_called_once_with("Expand G28: {}".format(expected))


class TestHookGcodeReceived(unittest.TestCase):

	def test_none(self):
		line = None
		p = RestoreLevelingAfterG28Plugin()
		actual = p.hook_gcode_received(None, line, None)
		self.assertEqual(line, actual, msg="line")
		self.assertFalse(p.leveling_enabled, msg="leveling enabled")

	def test_some_line(self):
		line = "Some line"
		p = RestoreLevelingAfterG28Plugin()
		actual = p.hook_gcode_received(None, line, None)
		self.assertEqual(line, actual, msg="line")
		self.assertFalse(p.leveling_enabled, msg="leveling enabled")

	def test_leveling_on(self):
		lines = ["echo:Bed Leveling On", "echo:Bed Leveling ON"]
		p = RestoreLevelingAfterG28Plugin()
		for line in lines:
			p._logger = MagicMock()
			actual = p.hook_gcode_received(None, line, None)
			self.assertEqual(line, actual, msg="line")
			self.assertTrue(p.leveling_enabled, msg="leveling enabled")
			p._logger.debug.assert_called_once_with("Leveling is enabled: True")

	def test_leveling_off(self):
		lines = ["echo:Bed Leveling Off", "echo:Bed Leveling OFF"]
		p = RestoreLevelingAfterG28Plugin()
		for line in lines:
			p._logger = MagicMock()
			actual = p.hook_gcode_received(None, line, None)
			self.assertEqual(line, actual, msg="line")
			self.assertFalse(p.leveling_enabled, msg="leveling enabled")
			p._logger.debug.assert_called_once_with("Leveling is enabled: False")
