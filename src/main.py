import time

from api.helpers.io_helper import scandir, rm_tree
from api.models.transfer import Transfer
from pathlib import Path


def main():
    p = Path(r'../testing')
    rm_tree(p/'B')
    (p / 'B').mkdir()
    contents = list(scandir(p, {'.txt'}, recursive=True))
    print(contents)
    tr = Transfer(contents, p/'B', verbose=True)
    tr.start()
    time.sleep(1)
    tr.stop()
    print()
    print(tr.progress)
    print()
    print()

    print()

    time.sleep(2)
    tr.start().join()  # wait till it finishes
    # if main thread ends before spawned thread -> error bc the manager does not exist anymore
    print(tr.progress)


if __name__ == '__main__':
    main()
