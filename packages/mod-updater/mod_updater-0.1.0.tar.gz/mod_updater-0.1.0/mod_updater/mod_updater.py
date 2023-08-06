from .parser import parse_config

def main():
    sources = parse_config()
    for source in sources:
        source.download()