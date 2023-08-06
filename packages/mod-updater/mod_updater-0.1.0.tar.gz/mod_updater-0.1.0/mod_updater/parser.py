import json
import os
from mod_updater.sources.github import GithubSource

source_type_mapping = {
    "GITHUB": GithubSource
}

def parse(config):
    if "mods_dir" not in config:
        raise Exception("Required mods_dir, this is the path to the mods directory")
    mods_path = config["mods_dir"]
    mod_sources = config["mods"]
    sources = []
    for s in mod_sources:
        source_type = s["source"]
        if source_type not in source_type_mapping:
            raise Exception("Invalid source type ", source_type)
        source_class = source_type_mapping[source_type]
        sources.append(source_class.parse(s, mods_path))
    return sources 

def parse_config(config_file="config.json"):
    if not os.path.exists(config_file):
        raise Exception("Cannot find config file ", config_file)
    with open(config_file) as f:
        config = json.load(f)
    return parse(config)


