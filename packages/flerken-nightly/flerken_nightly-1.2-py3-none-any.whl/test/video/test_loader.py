import unittest
import os
import shutil

import numpy as np
import cv2

from flerken.video import VideoSampler
from flerken.video.utils import apply_single


class TestLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.path = './videoplayback.mp4'
        self.folder_path = './tmp_f'
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)

    def tearDown(self) -> None:
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)

    def test_init(self):
        VideoSampler(1, 1)
        VideoSampler(2, 2)
        with self.assertRaises(AssertionError):
            VideoSampler(-1, 1)
        with self.assertRaises(AssertionError):
            VideoSampler(1, -1)
        with self.assertRaises(AssertionError):
            VideoSampler(1.5, 1)
        with self.assertRaises(AssertionError):
            VideoSampler(5, 1.2)

    def test_loading(self):
        sampler = VideoSampler(1, 5)

        os.mkdir(self.folder_path)
        # apply_single(self.path, 'tmp_f/%03d.bmp', [], [], None)
        # paths = sorted(os.listdir(self.folder_path))
        # paths = [os.path.join(self.folder_path, x) for x in paths]
        sampled_frames = sampler(self.path, 25)
        assert len(sampled_frames) == 5
        # frames = [cv2.imread(x)[..., ::-1] for x in paths[25:30]]
        # for sf, f in zip(sampled_frames, frames):
        #     assert (sf == f).all()
