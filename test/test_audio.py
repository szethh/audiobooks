from pathlib import Path

from api.helpers.io_helper import scandir
from api.helpers import audio_helper
import pytest


TEST_BOOK = Path('test_data/01 - The Colour Of Magic')


def test_get_chapters():
    files = list(scandir(TEST_BOOK, {'.mp3'}))
    chs, length = audio_helper.get_chapters(files)
    true_chs = [
                   {'title': 'DW01_01 Prologue', 'time': '0:00:00.000'},
                   {'title': 'DW01_02 Fire Roared Through The City', 'time': '0:04:22.363'}
    ]

    true_length = 262.363
    assert chs == true_chs
    assert true_length == pytest.approx(length)


def test_get_length():
    l1 = 262.363756
    file = TEST_BOOK / 'DW01_01 Prologue.mp3'
    l2 = audio_helper.get_length(file)
    assert l1 == pytest.approx(l2)
