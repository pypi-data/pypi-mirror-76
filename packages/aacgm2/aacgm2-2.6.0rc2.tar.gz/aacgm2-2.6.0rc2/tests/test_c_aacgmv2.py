from __future__ import division, print_function, absolute_import, unicode_literals

import numpy as np
import pytest

import aacgm2 as aacgmv2
from aacgm2._aacgmv2 import A2G, G2A, TRACE, BADIDEA, ALLOWTRACE, GEOCENTRIC


def test_module_structure():
    assert aacgmv2
    assert aacgmv2._aacgmv2
    assert aacgmv2._aacgmv2.setDateTime
    assert aacgmv2._aacgmv2.aacgmConvert


def test_constants():
    assert aacgmv2._aacgmv2.G2A == 0
    assert aacgmv2._aacgmv2.A2G == 1
    assert aacgmv2._aacgmv2.TRACE == 2
    assert aacgmv2._aacgmv2.ALLOWTRACE == 4
    assert aacgmv2._aacgmv2.BADIDEA == 8
    assert aacgmv2._aacgmv2.GEOCENTRIC == 16


def test_setDateTime():
    assert aacgmv2._aacgmv2.setDateTime(2013, 1, 1, 0, 0, 0) is None
    assert aacgmv2._aacgmv2.setDateTime(2015, 3, 4, 5, 6, 7) is None
    assert aacgmv2._aacgmv2.setDateTime(2017, 12, 31, 23, 59, 59) is None


def test_aacgmConvert_G2A_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A)
    np.testing.assert_almost_equal(mlat, 48.1902, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7505, decimal=4)
    np.testing.assert_almost_equal(r, 1.1775, decimal=4)

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A)
    np.testing.assert_almost_equal(mlat, 58.2194, decimal=4)
    np.testing.assert_almost_equal(mlon, 80.7282, decimal=4)
    np.testing.assert_almost_equal(r, 1.0457, decimal=4)


def test_aacgmConvert_A2G_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G)
    np.testing.assert_almost_equal(mlat, 30.7550, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1724, decimal=4)
    np.testing.assert_almost_equal(r, 1133.6246, decimal=4)

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G)
    np.testing.assert_almost_equal(mlat, 50.4371, decimal=4)
    np.testing.assert_almost_equal(mlon, -77.5323, decimal=4)
    np.testing.assert_almost_equal(r, 305.7308, decimal=4)


def test_aacgmConvert_G2A_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | TRACE)
    np.testing.assert_almost_equal(mlat, 48.1954, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7456, decimal=4)
    np.testing.assert_almost_equal(r, 1.1775, decimal=4)

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A | TRACE)
    np.testing.assert_almost_equal(mlat, 58.2189, decimal=4)
    np.testing.assert_almost_equal(mlon, 80.7362, decimal=4)
    np.testing.assert_almost_equal(r, 1.0457, decimal=4)


def test_aacgmConvert_A2G_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | TRACE)
    np.testing.assert_almost_equal(mlat, 30.7661, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1727, decimal=4)
    np.testing.assert_almost_equal(r, 1133.6282, decimal=4)

    aacgmv2._aacgmv2.setDateTime(2018, 1, 1, 0, 0, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G | TRACE)
    np.testing.assert_almost_equal(mlat, 50.4410, decimal=4)
    np.testing.assert_almost_equal(mlon, -77.5440, decimal=4)
    np.testing.assert_almost_equal(r, 305.7322, decimal=4)


def test_aacgmConvert_high_denied():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    np.testing.assert_equal(aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A),
        (np.nan, np.nan, np.nan))


def test_aacgmConvert_high_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A | TRACE)
    np.testing.assert_almost_equal(mlat, 59.9753, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7294, decimal=4)
    np.testing.assert_almost_equal(r, 1.8626, decimal=4)


def test_aacgmConvert_high_ALLOWTRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A | ALLOWTRACE)
    np.testing.assert_almost_equal(mlat, 59.9753, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7294, decimal=4)
    np.testing.assert_almost_equal(r, 1.8626, decimal=4)


def test_aacgmConvert_high_BADIDEA():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)
    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 5500, G2A | BADIDEA)
    np.testing.assert_almost_equal(mlat, 58.7286, decimal=4)
    np.testing.assert_almost_equal(mlon, 56.4296, decimal=4)
    np.testing.assert_almost_equal(r, 1.8626, decimal=4)


def test_aacgmConvert_GEOCENTRIC_G2A_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 48.3784, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7844, decimal=4)
    np.testing.assert_almost_equal(r, 1.1781, decimal=4)


def test_aacgmConvert_GEOCENTRIC_A2G_coeff():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 30.6117, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1724, decimal=4)
    np.testing.assert_almost_equal(r, 1135.0000, decimal=4)


def test_aacgmConvert_GEOCENTRIC_G2A_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, G2A | TRACE | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 48.3836, decimal=4)
    np.testing.assert_almost_equal(mlon, 57.7793, decimal=4)
    np.testing.assert_almost_equal(r, 1.1781, decimal=4)


def test_aacgmConvert_GEOCENTRIC_A2G_TRACE():
    aacgmv2._aacgmv2.setDateTime(2014, 3, 22, 3, 11, 0)

    mlat, mlon, r = aacgmv2._aacgmv2.aacgmConvert(45.5, -23.5, 1135, A2G | TRACE | GEOCENTRIC)
    np.testing.assert_almost_equal(mlat, 30.6227, decimal=4)
    np.testing.assert_almost_equal(mlon, -94.1727, decimal=4)
    np.testing.assert_almost_equal(r, 1135.0000, decimal=4)


def test_forbidden():
    np.testing.assert_equal(aacgmv2._aacgmv2.aacgmConvert(7, 0, 0, G2A),
        (np.nan, np.nan, np.nan))
