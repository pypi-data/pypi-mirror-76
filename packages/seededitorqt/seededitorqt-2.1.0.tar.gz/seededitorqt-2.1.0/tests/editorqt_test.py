#! /usr/bin/python
# -*- coding: utf-8 -*-
# from __future__ import print_function

# import funkcí z jiného adresáře
import sys
import os.path
import unittest
import scipy
import scipy.ndimage
import numpy as np
import logging

logger = logging.getLogger(__name__)
path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../src/"))
# from nose.plugins.attrib import attr
import pytest

# from pysegbase import pycut
import seededitorqt
import numpy as np
from PyQt5.QtWidgets import QApplication

# def fv_function(data, voxelsize, seeds=None, cls=None):
#     """
#     Creates feature vector for only data or for data from classes
#     """
#
#     fv1 = data.reshape(-1,1)
#
#     data2 = scipy.ndimage.filters.gaussian_filter(data, sigma=0.1)
#     fv2 = data2.reshape(-1,1)
#
#     fv = np.hstack([fv1, fv2])
#
#     if seeds is not None:
#         logger.debug("seeds " + str(seeds))
#         print("seeds ", seeds)
#         sd = seeds.reshape(-1,1)
#         selection = np.in1d(sd, cls)
#         fv = fv[selection]
#         sd = sd[selection]
#         # sd = sd[]
#         return fv, sd
#     return fv
#
# def box_data(noise_sigma=3):
#     # data
#     img3d = np.random.rand(32, 64, 64) * noise_sigma
#     img3d[4:24, 12:32, 5:25] = img3d[4:24, 12:32, 5:25] + 30
#
#     # seeds
#     seeds = np.zeros([32, 64, 64], np.int8)
#     seeds[9:12, 13:29, 18:25] = 1
#     seeds[9:12, 4:9, 3:32] = 2
#     # [mm]  10 x 10 x 10        # voxelsize_mm = [1, 4, 3]
#     voxelsize_mm = [5, 5, 5]
#     metadata = {'voxelsize_mm': voxelsize_mm}
#     return img3d, seeds, voxelsize_mm

class SeedEditorQtTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.version_info.major < 3:
            cls.assertCountEqual = cls.assertItemsEqual

    @pytest.mark.interactive
    def test_show_editor(self):
        """
        just run editor to see what is new
        Returns:
        """
        app = QApplication(sys.argv)
        data = (np.random.rand(30, 31, 32) * 100).astype(np.int)
        data[15:40, 13:20, 10:18] += 50
        se = seededitorqt.QTSeedEditor(data)
        se.exec_()
        # self.assertTrue(False)

    @pytest.mark.interactive
    def test_show_editor(self):
        """
        just run editor to see what is new
        Returns:
        """
        app = QApplication(sys.argv)
        data = (np.random.rand(30, 31, 32) * 100).astype(np.int)
        data[15:40, 13:20, 10:18] += 50
        se = seededitorqt.QTSeedEditor(data)

        se.exec_()

    # @pytest.mark.interactive
    def test_show_editor_with_seeds(self):
        """
        just run editor to see what is new
        Returns:
        """
        img, segm, seeds = self.make_data()
        app = QApplication(sys.argv)
        se = seededitorqt.QTSeedEditor(img, seeds=seeds)
        # se.exec_()
        assert np.max(se.seeds) > 0

    def test_show_editor_with_seeds_custom_colors(self):
        """
        just run editor to see what is new
        Returns:
        """
        img, segm, seeds = self.make_data()
        app = QApplication(sys.argv)
        seeds_colortable = seededitorqt.seed_editor_qt.SEEDS_COLORTABLE.copy()
        seeds_colortable[1] = [64, 255, 255, 60]
        se = seededitorqt.QTSeedEditor(img, seeds=seeds, contours=segm.astype(np.uint8), seeds_colortable=seeds_colortable)
        # se.exec_()
        assert se.slice_box.seeds_colortable[1][0] == 64
        assert np.max(se.seeds) > 0

    def test_show_draw_and_pickup_seed(self):
        """
        just run editor to see what is new
        Returns:
        """
        app = QApplication(sys.argv)
        data = (np.random.rand(30, 31, 32) * 100).astype(np.int)
        data[15:40, 13:20, 10:18] += 50
        se = seededitorqt.QTSeedEditor(data)
        se.slice_box.seed_mark = 3  # seed 3
        se.slice_box.last_position = [1, 3]
        se.slice_box.drawSeeds([10, 5])
        se.slice_box.seed_mark = 2  # left mouse button
        se.slice_box.last_position = [8, 1]
        se.slice_box.drawSeeds([7, 5])
        # try to pick up seed from slice
        se.slice_box._pick_up_seed_label([1, 3])
        self.assertEqual(se.textFocusedSeedLabel, "3", "Pickuped value")
        se.change_focus_seed_label(2)
        self.assertEqual(se.textFocusedSeedLabel, "2", "Changed value")
        # se.exec_()

    def test_show_draw_and_pickup_segmentation_label(self):
        """
        just run editor to see what is new
        Returns:
        """
        app = QApplication(sys.argv)
        data = (np.random.rand(30, 31, 32) * 100).astype(np.int)
        data[15:40, 13:20, 10:18] += 50
        segmentation = np.zeros_like(data)
        segmentation[15:40, 13:20, 10:18] = 1
        se = seededitorqt.QTSeedEditor(data, contours=segmentation)
        se.selectSlice(20)
        se.slice_box.seed_mark = 3  # seed 3
        se.slice_box.last_position = [1, 3]
        se.slice_box.drawSeeds([10, 5])
        se.slice_box.seed_mark = 2  # left mouse button
        se.slice_box.last_position = [8, 1]
        se.slice_box.drawSeeds([7, 5])
        # try to pick up seed from slice
        se.slice_box._pick_up_segmentation_label([16, 16])
        # self.assertEqual(se.textFocusedSeedLabel, "3", "Pickuped value")
        idx = se.combo_segmentation_label.currentIndex()
        logger.debug("idx {}".format(idx))
        self.assertEqual(idx, 1, "Picked up value")
        se.change_focus_segmentation_label(0)
        idx = se.combo_segmentation_label.currentIndex()
        logger.debug("idx {}".format(idx))
        self.assertEqual(idx, 0, "Changed value")
        # se.exec_()

    # @attr("interactive")
    @pytest.mark.interactive
    def test_show_editor_with_too_much_wide_data(self):
        """
        just run editor to see what is new
        Returns:
        """
        app = QApplication(sys.argv)
        data = (np.random.rand(30, 31, 150) * 100).astype(np.int)
        data[15:40, 13:20, 10:18] += 50
        se = seededitorqt.QTSeedEditor(data)
        se.exec_()

    # @attr('interactive')
    def test_draw_seed_function(self):
        """
        just run editor to see what is new
        Returns:
        """
        app = QApplication(sys.argv)
        data = (np.random.rand(30, 31, 32) * 100).astype(np.int)
        data[15:40, 13:20, 10:18] += 50
        se = seededitorqt.QTSeedEditor(data)
        se.slice_box.seed_mark = 1  # left mouse button
        se.slice_box.last_position = [1, 3]
        se.slice_box.drawSeeds([10, 5])
        se.slice_box.seed_mark = 2  # left mouse button
        se.slice_box.last_position = [8, 1]
        se.slice_box.drawSeeds([7, 5])
        # se.exec_()

    # @TODO znovu zprovoznit test
    # @unittest.skip("Cekame, az to Tomas opravi")
    def make_data(self, sz=32, offset=0, sigma=80):
        seeds = np.zeros([sz, sz, sz], dtype=np.int8)
        seeds[offset + 12, offset + 9 : offset + 14, offset + 10] = 1
        seeds[offset + 20, offset + 18 : offset + 21, offset + 12] = 1
        img = np.ones([sz, sz, sz])
        img = img - seeds
        seeds[
            offset + 3 : offset + 15, offset + 2 : offset + 6, offset + 27 : offset + 29
        ] = 2
        img = scipy.ndimage.morphology.distance_transform_edt(img)
        segm = img < 7
        img = (100 * segm + sigma * np.random.random(img.shape)).astype(np.uint8)
        return img, segm, seeds


if __name__ == "__main__":
    unittest.main()
