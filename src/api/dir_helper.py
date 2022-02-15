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


async def transfer(source, destination, move=False, cancel=False, **kwargs):
    """
    Moves (or copies) files.
    :param source: An iterable containing the files to transfer.
    :param destination: The directory to transfer the files to.
    :param move: Whether to remove or the file after transfer.
    :param cancel: If true, stops the transferring loop.
    For use in a generator context where the function is called multiple times.
    :return: A generator with the progress. FIXME: maybe it's better to have a dict????
    """

    for file in source:
        status = 'incomplete'
        if cancel: break

        f = open(destination, 'ab+')
        while True:
            data = read_chunk(file, **kwargs)
            if not data:
                break
            destination.write(data)

        status = 'complete'
        yield file, status


# def copy_file(f1, f2, cancel=False):
#     while not cancel:
#         data = read_chunk(file, **kwargs)
#         if not data:
#             break
#         destination.write(data)


# https://stackoverflow.com/a/519653
def read_chunk(file, chunk_size=16384):
    """
    Reads a file in chunks (16kb by default)
    """
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data
        #break  # prevent any errors with file handling


def move(source, destination):
    return transfer(source, destination, True)


def copy(source, destination):
    return transfer(source, destination, False)


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()
