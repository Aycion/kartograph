from pathlib import Path
import re

__all__ = ['DEFAULT_IMAGE_DIR', 'enumerate_basename']


DEFAULT_IMAGE_DIR = (Path(__file__).parent.parent / '../images').resolve()


def enumerate_basename(_dir, basename):
    """

    :param Path _dir:
    :param str basename:
    :return:
    """
    _dir = Path(_dir)
    if not _dir.is_absolute():
        _dir = DEFAULT_IMAGE_DIR / Path(_dir)
    _dir.mkdir(parents=True, exist_ok=True)
    path = _dir / basename

    if not path.exists():
        return path
    name, ext = basename.rsplit('.', 1)
    mat = re.match(r'\D+(\d+)$', name)
    if mat:
        i = int(mat.group(1))
    else:
        i = 1
    while path.with_name(f'{name}-{i}.{ext}').exists():
        i += 1
    return path.with_name(f'{name}-{i}.{ext}')
