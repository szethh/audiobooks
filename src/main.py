import time

from api.dir_helper import scandir, rm_tree
from api.transfer import Transfer
from pathlib import Path


def main():
    p = Path(r'../testing')
    rm_tree(p/'B')
    (p / 'B').mkdir()
    contents = list(scandir(p, {'.txt'}, recursive=True))
    print(contents)
    tr = Transfer(contents, p/'B')
    tr.start()
    time.sleep(1)
    print('uwu')
    tr.stop()
    print('stopped')


if __name__ == '__main__':
    main()
