import datetime
from pathlib import Path

import ffmpeg
import subprocess


def ff_mp3merge(files, output):
    output += '.mp3'
    (
        ffmpeg
        .input(f'concat:{"|".join(files)}', vn=None)
        .output(str(output), acodec='copy')
        .global_args('-loglevel', 'error')
        .overwrite_output()
        .run()
    )
    return output


def ff_mp3_m4a(mp3, output):
    output += '.m4a'
    (
        ffmpeg
        .input(mp3)
        .output(output, acodec='aac', **{'vn': None}, **{'b:a': 64}, **{'ac': 2})
        .global_args('-loglevel', 'error')
        .overwrite_output()
        .run()
    )
    return output


def ff_mp4_m4a(mp4, output):
    output += '.m4a'
    (
        ffmpeg
        .input(mp4)
        .output(output, acodec='copy')
        .global_args('-loglevel', 'error')
        .overwrite_output()
        .run()
    )
    return output


def ff_m4a_m4b(m4a, metadata, output):
    output += '.m4b'
    m4a = ffmpeg.input(m4a)
    metadata = ffmpeg.input(metadata)
    cmd = (
        m4a
        .output(metadata, output, map_metadata='1')
        .global_args('-loglevel', 'error')
        .overwrite_output()
        .compile()
    )
    while '-map' in cmd:
        idx = cmd.index('-map')
        cmd.pop(idx)
        cmd.pop(idx)

    # print(cmd)
    subprocess.call(cmd)

    # (
    #     m4a
    #     .output(metadata, output, map_metadata='1')
    #     .overwrite_output()
    #     .run()
    # )
    return output


def mp3_metadata(files, output):
    chaps, length = get_chapters(files)
    metadata = get_metadata(chaps, length)
    meta = Path(output) / 'metadata'
    with open(meta, 'w+') as f:
        f.write(metadata)
    return meta


def get_length(file):
    return float(ffmpeg.probe(file)['format']['duration'])


def get_chapters(files):
    chapters = []
    timestamp = 0
    for file in files:
        file = Path(file)
        audio_length = get_length(file)

        t = format_time(timestamp)
        title = file.stem

        chapters.append({'title': title, 'time': t})
        timestamp = timestamp + audio_length
    return chapters, timestamp


def get_metadata(chapters, length):
    metadata = ";FFMETADATA1"
    for i in range(len(chapters) - 1):
        chap = chapters[i]
        title = chap['title']
        start = parse_time(chap['time'])
        end = parse_time(chapters[i + 1]['time']) - 1
        metadata += f"\n[CHAPTER]\nTIMEBASE=1/1\nSTART={start}\nEND={end}\ntitle={title}"

    # set to correct format
    length = parse_time(format_time(length))
    metadata += \
        f"\n[CHAPTER]\nTIMEBASE=1/1\nSTART={parse_time(chapters[-1]['time'])}" \
        f"\nEND={length}\ntitle={chapters[-1]['title']}"

    return metadata


def format_time(t):
    t = str(datetime.timedelta(seconds=t))
    idx = t.find('.')
    if idx == -1:  # if there are no second decimals, we add them for consistency
        t += '.000'
    else:
        t = t[:idx + 4]  # truncate seconds to 3 decimals
    return t


def parse_time(t):
    t = datetime.datetime.strptime(t, '%H:%M:%S.%f').time()
    return (t.hour * 60 + t.minute) * 60 + t.second + t.microsecond * 1e-6
