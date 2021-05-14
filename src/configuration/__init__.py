import yaml
from pathlib import Path

__all__ = ["CONFIG"]


def load_configuration():
    cfgFile = Path(__file__).parent/"configuration.yml"
    return yaml.load(cfgFile.open("r"), Loader=yaml.Loader)


CONFIG = load_configuration()
