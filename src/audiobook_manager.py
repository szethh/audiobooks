from pathlib import Path
from api.helpers import io_helper
from api.models.transfer import Transfer


class AudiobookManager:
    def __init__(self, original, temp, audiobooks):
        self.original = Path(original)
        self.temp = Path(temp)
        self.audiobooks = Path(audiobooks)

    def scan_original(self):
        files = io_helper.scandir(self.original, {'.mp3', '.m4a', '.m4b', '.mp4', '.ogg'})
        # filter files using db of already processed files

        tr = Transfer(files, self.temp)
        # tr.start()  # we need a way to await it or leave it in the bg while also retrieving progress
