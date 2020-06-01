import unittest

from mock import MagicMock

from octoprint_restore_leveling_after_g28 import RestoreLevelingAfterG28Plugin


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
		p._logger.info = MagicMock()
		actual = p.hook_gcode_received(None, line, None)
		self.assertEqual(line, actual, msg="line")
		self.assertTrue(p.leveling_enabled, msg="leveling enabled")
		p._logger.info.assert_called_once_with("Leveling is enabled: True")

	def test_leveling_off(self):
		line = "echo:Bed Leveling Off"
		p = RestoreLevelingAfterG28Plugin()
		p._logger = MagicMock()
		p._logger.info = MagicMock()
		actual = p.hook_gcode_received(None, line, None)
		self.assertEqual(line, actual, msg="line")
		self.assertFalse(p.leveling_enabled, msg="leveling enabled")
		p._logger.info.assert_called_once_with("Leveling is enabled: False")
