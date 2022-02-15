import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
import threading
import multiprocessing as mp
import src.api.dir_helper as dir_helper
import time
from pathlib import Path


class Transfer:
    progress = {}
    cancel = False
    remaining = []
    task = None
    file = None

    def __init__(self, source, destination, move=False, chunk_size=16384):
        self.source = list(source)
        self.destination = destination
        self.move = move
        self.chunk_size = chunk_size

    def get_remaining(self):
        self.remaining = [(x, *self.get_progress(x)) for x in self.source if self.get_progress(x)[0] != 'complete']
        return self.remaining

    def get_destination(self, file):
        dest = Path(self.destination) / Path(file).name
        # check if exists maybe
        return dest

    def get_next(self):
        if len(self.remaining) > 0:
            return self.remaining[0]

    def get_file(self):
        file = self.get_next()

    def start(self):
        self.get_remaining()  # update remaining list
        print('starting transfer')
        self.cancel = mp.Event()
        self.task = mp.Process(target=self.loop, args=(self.cancel,))
        self.task.start()

    def loop(self, stop):
        def step():
            if not self.cancel.is_set():
                dest = self.get_destination(file)
                with open(dest, 'ab+') as f2:
                    data = next(dir_helper.read_chunk(f1, self.chunk_size), None)
                    if data:
                        f2.write(data)
                    else:  # there is no data to read -- we finished a file
                        if Path(file).stat().st_size != dest.stat().st_size:
                            raise IOError(f'Error while copying file: input and output size did not match '
                                          f'({Path(file).stat().st_size} vs {dest.stat().st_size}).')

                        print(f'Completed copying file {file}')
                        self.progress[file] = ('complete', int(time.time() * 1000))
                        self.get_remaining()  # we refresh

        while True:
            file = self.get_next()  # get next incomplete file
            if not file:
                break
            file = file[0]
            with open(file, 'rb') as f1:
                step()

        print('Transfer finished!!')
        stop.set()

    def get_progress(self, file):
        return self.progress.get(file, ('incomplete', int(time.time() * 1000)))

    def stop(self):
        print('stopping transfer')
        self.cancel.set()
        self.task.terminate()


