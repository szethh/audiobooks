import time
from api.helpers.io_helper import scandir
from api.models.audio_maps import *


class Audiobook:
    """
    * For each directory __mp3_dir__:
      * Find all mp3s
      * Probe first to get bitrate
      * Call docker to merge all mp3s into a chapterized m4b, store it in __m4b_dir__
      * Move chapters.txt file into __m4b_dir__/chapters
      * Delete old mp3 folder (__mp3_dir__)
    """
    def __init__(self, book_dir):
        self.book_dir = Path(book_dir)
        self.output = self.book_dir.parent / self.book_dir.stem
        self.pipeline = []
        self.files = []

    def convert_book(self, x=None):
        self.files = sorted(scandir(self.book_dir, {'.mp3'}))

        if not x:
            x = {'inp': [str(f.as_posix()) for f in self.files]}  # merge input

        # this should be format-specific -- a subclass maybe?
        self.pipeline = [
            MP3ToMetadata(self.output, keep=True),
            MP3Merge(self.output),
            MP3ToM4A(self.output),
            M4AToM4B(self.output, keep=True)
        ]

        print(f'Starting process for book {self.output.stem}')
        for i, s in enumerate(self.pipeline):
            print(f'Step [{i+1}/{len(self.pipeline)}] {s.__class__.__name__} with input {x}')
            start = time.time()
            x = s(**x)
            print(f'Took {time.time()-start}s, left {len(s.cleanup)} leftovers')

        print('Done! Removing leftovers now...')
        s = self.pipeline[-1]
        print(f'Cleaning up to {s.__class__.__name__}: {s.cleanup}')
        s.clean()

        return x
