import unittest
from parser import parse, parse_config
import json
import os

class TestParser(unittest.TestCase):

    def test_parse_sources(self):
        config = {
            "mods_dir": "mods",
            "mods": [
                {
                    "source": "GITHUB",
                    "owner": "snallapa",
                    "repo": "scentfindermod"
                }
            ]
        }
        sources = parse(config)
        self.assertEqual(1, len(sources))
        self.assertEqual("GithubSource", sources[0].__class__.__name__)

    def test_parse_fails_missing_dir(self):
        config = {}
        self.assertRaises(Exception, parse, config)

    def test_parse_fails_invalid_source(self):
        config = {
            "mods_dir": "mods",
            "mods": [
                {
                    "source": "foo",
                }
            ]
        }
        self.assertRaises(Exception, parse, config)

    def test_parse_reads_file(self):
        config = {
            "mods_dir": "mods",
            "mods": [
                {
                    "source": "GITHUB",
                    "owner": "snallapa",
                    "repo": "scentfindermod"
                }
            ]
        }
        with open('config.json', 'w') as outfile:
            json.dump(config, outfile)
        
        def cleanup():
            os.remove("config.json")
        self.addCleanup(cleanup)
        sources = parse_config()
        self.assertEqual(1, len(sources))
        self.assertEqual("GithubSource", sources[0].__class__.__name__)
