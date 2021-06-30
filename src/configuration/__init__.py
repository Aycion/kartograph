import yaml
from pathlib import Path

from .parameters import GlobalParameters


def get_root_context():
    return _ROOT_CONTEXT


__all__ = ['CONFIG', 'GlobalParameters', 'get_root_context']


def load_configuration():
    cfg_yml = Path(__file__).parent/'configuration.yml'
    return yaml.load(cfg_yml.open('r'), Loader=yaml.Loader)


CONFIG = load_configuration()
_ROOT_CONTEXT = GlobalParameters(CONFIG)