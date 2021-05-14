from pathlib import Path
import re

__all__ = ['DEFAULT_BUILD_DIR', 'validate_fname']


DEFAULT_BUILD_DIR = (Path(__file__).parent.parent / '../images').resolve()


def validate_fname(_dir, fname):
    """

    :param Path _dir:
    :param str fname:
    :return:
    """
    if not _dir.is_absolute():
        _dir = DEFAULT_BUILD_DIR / Path(_dir)
    path = _dir / fname
    if not path.exists():
        return path
    name, ext = fname.rsplit('.', 1)
    mat = re.match(r'\D+(\d+)$', name)
    if mat:
        i = int(mat.group(1))
    else:
        i = 1
    while path.with_name(f'{name}-{i}.{ext}').exists():
        i += 1
    return path.with_name(f'{name}-{i}.{ext}')
