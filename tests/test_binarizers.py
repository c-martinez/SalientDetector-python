# -*- coding: utf-8 -*-
from .context import salientregions as sr
import unittest
import cv2
import os

class ThresholdBinarizerTester(unittest.TestCase):
    '''
    Tests for the helper functions related to images
    '''

    def setUp(self):
        testdata_path = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                '../../../TestData/Gray/'))
        self.image = cv2.imread(os.path.join(testdata_path, 'Gray_scale.png'))
        self.binarized_true_175 = cv2.imread(
                os.path.join(
                    testdata_path,
                    'Binarized_thresh175.png'), cv2.IMREAD_GRAYSCALE)
        self.threshold175 = sr.ThresholdBinarizer(175)
        self.binarized_true_57 = cv2.imread(
                os.path.join(
                    testdata_path,
                    'Binarized_thresh57.png'), cv2.IMREAD_GRAYSCALE)
        self.threshold57 = sr.ThresholdBinarizer(57)
        self.binarized_true_0 = cv2.imread(
                os.path.join(
                    testdata_path,
                    'Binarized_thresh0.png'), cv2.IMREAD_GRAYSCALE)
        self.threshold0 = sr.ThresholdBinarizer(0)
        self.binarized_true_255 = cv2.imread(
                os.path.join(
                    testdata_path,
                    'Binarized_thresh255.png'), cv2.IMREAD_GRAYSCALE)
        self.threshold255 = sr.ThresholdBinarizer(255)
        self.threshold256 = sr.ThresholdBinarizer(256)
        self.thresholdneg1 = sr.ThresholdBinarizer(-1)

    def test_binarize175(self):
        binarized = self.threshold175.binarize(self.image, visualize=False)
        assert sr.image_diff(
            self.binarized_true_175,
            binarized,
            visualize=False)

    def test_binarize57(self):
        binarized = self.threshold57.binarize(self.image, visualize=False)
        assert sr.image_diff(
            self.binarized_true_57,
            binarized,
            visualize=False)

    def test_binarize0(self):
        binarized = self.threshold0.binarize(self.image, visualize=False)
        assert sr.image_diff(self.binarized_true_0, binarized, visualize=False)

    def test_binarize255(self):
        binarized = self.threshold255.binarize(self.image, visualize=False)
        assert sr.image_diff(
            self.binarized_true_255,
            binarized,
            visualize=False)
            
    # Edge cases: if threshold outside of allowed range, it should be capped
    def test_binarize256(self):
        binarized = self.threshold256.binarize(self.image, visualize=False)
        assert sr.image_diff(
            self.binarized_true_255,
            binarized,
            visualize=False)

    def test_binarizeneg1(self):
        binarized = self.thresholdneg1.binarize(self.image, visualize=False)
        assert sr.image_diff(
            self.binarized_true_0,
            binarized,
            visualize=False)