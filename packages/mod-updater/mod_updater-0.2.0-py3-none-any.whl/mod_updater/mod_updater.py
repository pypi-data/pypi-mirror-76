from .parser import parse_config
import argparse

def main():
    parser = argparse.ArgumentParser(description='config path')
    parser.add_argument('--config', metavar='config_path', type=str, default="config.json")
    args = parser.parse_args()
    sources = parse_config(args.config)
    for source in sources:
        source.download()