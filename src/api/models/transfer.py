import shutil
import multiprocessing as mp
import time
from pathlib import Path


class Transfer:
    def __init__(self, source, destination, move=False, verbose=False):
        manager = mp.Manager()
        self.loop = None
        self.source = source
        self.destination = destination
        self.move = move
        self.verbose = verbose
        self.progress = manager.dict()
        self.task = None
        self.remaining = []

    def get_remaining(self):
        self.remaining = [x for x in self.source if self.get_progress(str(x))[0] != 'complete']
        return self.remaining

    def get_destination(self, file):
        dest = Path(self.destination) / Path(file).name
        # check if exists maybe
        return dest

    def start(self):
        self.get_remaining()  # update remaining list
        if self.verbose:
            print(f'Starting transfer - {len(self.remaining)} remaining files.')
        self.task = mp.Process(target=self.run)
        self.task.start()
        return self.task

    def stop(self):
        if self.verbose:
            print('\nStopping transfer...', end='')
        self.task.terminate()
        if self.verbose:
            print(' done!')

    def run(self):
        self.get_remaining()
        total = current = len(self.remaining)
        while current > 0:
            file = self.remaining[0]
            dest = self.get_destination(file)
            if self.verbose:
                print(f'[{total - current + 1}/{total}] Copying file {file} to {dest}...', end='')

            shutil.copy(file, dest)
            self.progress[str(file)] = ('complete', int(time.time() * 1000))
            self.get_remaining()
            if self.verbose:
                print(' done!')
            current = len(self.remaining)
            #yield self.progress

        if self.verbose:
            print('Transfer finished!!')

    def get_progress(self, file):
        return self.progress.get(str(file), ('incomplete', int(time.time() * 1000)))
