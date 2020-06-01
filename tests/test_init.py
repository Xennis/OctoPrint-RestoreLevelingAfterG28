import unittest

from mock import MagicMock

from octoprint_restore_leveling_after_g28 import RestoreLevelingAfterG28Plugin


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
		actual = p.hook_atcommand_sending(None, None, cmd, None, tags=["tag1", "tag2"])
		self.assertIsNone(actual)
		p._logger.info.assert_called_once_with("Re-enable leveling: M420 S1")
		p._printer.commands.assert_called_once_with("M420 S1", tags=["tag1", "tag2"])

	def test_cmd_leveling_on_tags_none(self):
		cmd = "restore_leveling"
		p = RestoreLevelingAfterG28Plugin()
		p.leveling_enabled = True
		p._logger = MagicMock()
		p._printer = MagicMock()
		actual = p.hook_atcommand_sending(None, None, cmd, None, tags=None)
		self.assertIsNone(actual)
		p._logger.info.assert_called_once_with("Re-enable leveling: M420 S1")
		p._printer.commands.assert_called_once_with("M420 S1", tags=None)


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
		line = "echo:Bed Leveling On"
		p = RestoreLevelingAfterG28Plugin()
		p._logger = MagicMock()
		actual = p.hook_gcode_received(None, line, None)
		self.assertEqual(line, actual, msg="line")
		self.assertTrue(p.leveling_enabled, msg="leveling enabled")
		p._logger.info.assert_called_once_with("Leveling is enabled: True")

	def test_leveling_off(self):
		line = "echo:Bed Leveling Off"
		p = RestoreLevelingAfterG28Plugin()
		p._logger = MagicMock()
		actual = p.hook_gcode_received(None, line, None)
		self.assertEqual(line, actual, msg="line")
		self.assertFalse(p.leveling_enabled, msg="leveling enabled")
		p._logger.info.assert_called_once_with("Leveling is enabled: False")
