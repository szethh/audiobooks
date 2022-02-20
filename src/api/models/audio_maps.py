from pathlib import Path

from api.helpers.audio_helper import ff_m4a_m4b, ff_mp4_m4a, ff_mp3_m4a, mp3_metadata, ff_mp3merge


class AudioMap:
    def __init__(self, out, keep=False):
        self.out = str(out)
        self.keep = keep
        self.cleanup = []

    def __call__(self, inp, cleanup=None, **kwargs):
        self.cleanup = cleanup or []
        if not self.keep:
            if isinstance(inp, list):
                self.cleanup.extend(*[inp])
            else:
                self.cleanup.append(inp)

        return {'inp': inp, 'cleanup': self.cleanup, **kwargs}

    def clean(self):
        for f in self.cleanup:
            f = Path(f)
            if f.exists() and f.is_file():
                f.unlink()


class MP3Merge(AudioMap):
    def __call__(self, inp, **kwargs):
        return super(MP3Merge, self).__call__(ff_mp3merge(inp, self.out), **kwargs)


class MP3ToMetadata(AudioMap):
    def __call__(self, inp, **kwargs):
        # here we don't actually want to pass the metadata as input, but as another param
        return super(MP3ToMetadata, self).__call__(inp=inp, metadata=mp3_metadata(inp, self.out), **kwargs)


class MP3ToM4A(AudioMap):
    def __call__(self, inp, **kwargs):
        return super(MP3ToM4A, self).__call__(ff_mp3_m4a(inp, self.out), **kwargs)


class MP4ToM4A(AudioMap):
    def __call__(self, inp, **kwargs):
        return super(MP4ToM4A, self).__call__(ff_mp4_m4a(inp, self.out), **kwargs)


class M4AToM4B(AudioMap):
    def __call__(self, inp, **kwargs):
        if 'cleanup' in kwargs:
            kwargs['cleanup'] += [kwargs['metadata']]
        return super(M4AToM4B, self).__call__(ff_m4a_m4b(inp, kwargs['metadata'], self.out), **kwargs)
