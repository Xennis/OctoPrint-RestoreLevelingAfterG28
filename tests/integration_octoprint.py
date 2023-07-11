import time
import unittest
from pathlib import Path

from testcontainers.compose import DockerCompose


class TestIntegration(unittest.TestCase):

	def test_octoprint_boots_without_errors(self):
		project_root = Path(__file__).parent.parent
		with DockerCompose(str(project_root)) as compose:
			time.sleep(6)  # Give OctoPrint time to boot
			stdout, stderr = compose.get_logs()
			self.assertEqual(b"", stderr, msg="empty stderr")
			print(stdout.decode())
			self.assertTrue(b"|  Restore Leveling After G28" in stdout, msg="plugin was registered")
