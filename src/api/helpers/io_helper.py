from pathlib import Path


def scandir(path, extensions=None, recursive=False):
    """
    :param path: The path to scan
    :param extensions: The extensions to look for.
    :param recursive: Whether to traverse subfolders.
    :return: A generator with the results.
    """
    if extensions is None:
        extensions = {''}

    if recursive:
        return (p.resolve() for p in Path(path).rglob('*') if p.suffix in extensions)
    return (p.resolve() for p in Path(path).glob('*') if p.suffix in extensions)


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()
