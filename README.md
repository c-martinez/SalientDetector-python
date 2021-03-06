# Python software for image processing
[![Build Status](https://travis-ci.org/NLeSC/SalientDetector-python.svg?branch=master)](https://travis-ci.org/NLeSC/SalientDetector-python) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/1c9f59fcbc6d48bbb35addc7d51e0bf1)](https://www.codacy.com/app/d-vankuppevelt/SalientDetector-python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NLeSC/SalientDetector-python&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/1c9f59fcbc6d48bbb35addc7d51e0bf1)](https://www.codacy.com/app/d-vankuppevelt/SalientDetector-python?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NLeSC/SalientDetector-python&amp;utm_campaign=Badge_Coverage)

This folder contains a Python  implementation of the Salient Region Detector code as part of the [image processing part of eStep](https://www.esciencecenter.nl/technology/expertise/computer-vision). The software conforms with the [eStep standards](https://github.com/NLeSC/estep-checklist).

The original MATLAB implementation can be found at [this repository](https://github.com/NLeSC/SalientDetector-matlab)

Documentation can be found on [Read the Docs](http://salientdetector-python.readthedocs.io/).

The repository contains the following sub-folders:

## Notebooks
Several iPython notebooks testing and illustrating major functionality.

## salientregions
The module for salient region detection functionality.

## tests
Unit tests for the code in salientregions.

# Installation
## Prerequisites
* Python 2.7 or 3.5
* pip
* The python packages in `requirements.txt`.
* OpenCV 3.1. There is two ways to install OpenCV:
  * If you're using Conda, you can install OpenCV with the following command:

  `conda install -c https://conda.anaconda.org/menpo opencv3`

  * Otherwise, follow the instructions to [install OpenCV 3.1.0 manually](http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup)


## Installing the package
To install the package `salientregions`  in your environment:

`pip install .`

To perform tests:

`nosetests test`

# Getting started
The source code documentation can be found [here](http://salientdetector-python.readthedocs.io/)

This code makes heavily use of the OpenCV library, so in order to understand how the code works, it helps to have a look at the [OpenCV Documentation](http://docs.opencv.org/3.1.0/).

## Images
In OpenCV, images are represented as numpy arrays. Grayscale images are represented by a 2-dimensional array. Color images have a third dimension for the color channel. The Salient Region Detector has a few simplifying assumptions:
* Color images have BGR channels
* Images are assumed to be 8-bit. This is also the case for binary images, so they only have values of 0 and 255.

## Detector object
The complete functionality of the salient region detectors are found in the Detector object. The SalientDetector implements DMSR detection, and MSSRDetector implements MSSR detection (see referred papers for more information about these algorithms).
An example of how to use the Detector can be found in [this iPython Notebook](https://github.com/NLeSC/SalientDetector-python/blob/master/Notebooks/DetectorExample.ipynb).

# Contributing
If you want to contribute to the code, please have a look at the [eStep standarts](https://github.com/NLeSC/estep-checklist).

We use numpy-style code documentation.

# References
Ranguelova, E.B. - Pauwels, E.J.
Morphology-based Stable Salient Regions Detector
Proceedings of International Conference on Image and Vision Computing New Zealand 2006 , Great Barrier Island, New Zealand, p.97–102
