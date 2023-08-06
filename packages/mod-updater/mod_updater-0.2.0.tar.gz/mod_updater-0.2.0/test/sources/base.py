import unittest
import os
import shutil

class SourceTest(unittest.TestCase):
    TEST_MODS_FOLDER = "test_mods"

    def tearDown(self):
        if os.path.exists(self.TEST_MODS_FOLDER) and os.path.isdir(self.TEST_MODS_FOLDER):
            shutil.rmtree(self.TEST_MODS_FOLDER)