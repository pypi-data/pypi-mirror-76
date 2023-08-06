# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

import datetime as dt

import numpy as np
import pytest

import aacgm2 as aacgmv2
from aacgm2._aacgmv2 import A2G, G2A, TRACE, BADIDEA, ALLOWTRACE, GEOCENTRIC

date = (2015, 1, 1, 0, 0, 0)
dtObj = dt.datetime(*date)


def test_module_structure():
    assert aacgmv2
    assert aacgmv2.convert
    assert aacgmv2.convert_mlt
    assert aacgmv2.subsol
    assert aacgmv2.set_coeff_path
    assert aacgmv2.AACGM_v2_DAT_PREFIX
    assert aacgmv2.IGRF_12_COEFFS


def test_output_type():
    lat, lon, alt = aacgmv2.convert(60, 0, 300, dtObj)
    print(type(lat))
    print(lat.shape)
    print(lat.size)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)
    assert isinstance(alt, np.ndarray)

    lat, lon, alt = aacgmv2.convert([60], [0], [300], dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)
    assert isinstance(alt, np.ndarray)

    lat, lon, alt = aacgmv2.convert([60, 61], [0, 0], [300, 300], dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)
    assert isinstance(alt, np.ndarray)

    lat, lon, alt = aacgmv2.convert([60, 61, 62], 0, 300, dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)
    assert isinstance(alt, np.ndarray)

    lat, lon, alt = aacgmv2.convert(np.array([60, 61, 62]), 0, 300, dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)
    assert isinstance(alt, np.ndarray)

    lat, lon, alt = aacgmv2.convert(np.array([[60, 61, 62], [63, 64, 65]]), 0, 300, dtObj)
    assert isinstance(lat, np.ndarray)
    assert isinstance(lon, np.ndarray)
    assert isinstance(alt, np.ndarray)


def test_output_shape_size():
    lat, lon, alt = aacgmv2.convert(60, 0, 300, dtObj)
    assert lat.shape == tuple()
    assert lon.shape == tuple()
    assert alt.shape == tuple()
    assert lat.size == 1
    assert lon.size == 1
    assert alt.size == 1

    lat, lon, alt = aacgmv2.convert([60], [0], [300], dtObj)
    assert lat.shape == (1,)
    assert lon.shape == (1,)
    assert alt.shape == (1,)
    assert lat.size == 1
    assert lon.size == 1
    assert alt.size == 1

    lat, lon, alt = aacgmv2.convert([60, 61], [0, 0], [300, 300], dtObj)
    assert lat.shape == (2,)
    assert lon.shape == (2,)
    assert alt.shape == (2,)
    assert lat.size == 2
    assert lon.size == 2
    assert alt.size == 2

    lat, lon, alt = aacgmv2.convert([60, 61, 62], 0, 300, dtObj)
    assert lat.shape == (3,)
    assert lon.shape == (3,)
    assert alt.shape == (3,)
    assert lat.size == 3
    assert lon.size == 3
    assert alt.size == 3

    lat, lon, alt = aacgmv2.convert(np.array([60, 61, 62]), 0, 300, dtObj)
    assert lat.shape == (3,)
    assert lon.shape == (3,)
    assert alt.shape == (3,)
    assert lat.size == 3
    assert lon.size == 3
    assert alt.size == 3

    lat, lon, alt = aacgmv2.convert(np.array([[60, 61, 62],
                                         [63, 64, 65]]),
                               0, 300, dtObj)
    assert lat.shape == (2, 3)
    assert lon.shape == (2, 3)
    assert alt.shape == (2, 3)
    assert lat.size == 6
    assert lon.size == 6
    assert alt.size == 6


def test_convert_result_values_shape():
    lat, lon, alt = aacgmv2.convert(np.array([[60, 61, 62],
                                         [63, 64, 65]]),
                               0, 300, dtObj)
    aacgmv2._aacgmv2.setDateTime(*date)
    np.testing.assert_allclose((lat[0, 0], lon[0, 0], alt[0, 0]),
            aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A), rtol=1e-5)
    np.testing.assert_allclose((lat[0, 1], lon[0, 1], alt[0, 1]),
            aacgmv2._aacgmv2.aacgmConvert(61, 0, 300, G2A), rtol=1e-5)
    np.testing.assert_allclose((lat[0, 2], lon[0, 2], alt[0, 2]),
            aacgmv2._aacgmv2.aacgmConvert(62, 0, 300, G2A), rtol=1e-5)
    np.testing.assert_allclose((lat[1, 0], lon[1, 0], alt[1, 0]),
            aacgmv2._aacgmv2.aacgmConvert(63, 0, 300, G2A), rtol=1e-5)
    np.testing.assert_allclose((lat[1, 1], lon[1, 1], alt[1, 1]),
            aacgmv2._aacgmv2.aacgmConvert(64, 0, 300, G2A), rtol=1e-5)
    np.testing.assert_allclose((lat[1, 2], lon[1, 2], alt[1, 2]),
            aacgmv2._aacgmv2.aacgmConvert(65, 0, 300, G2A), rtol=1e-5)


def test_convert_datetime_date():
    lat_1, lon_1, alt_1 = aacgmv2.convert(60, 0, 300, dt.date(2013, 12, 1))
    lat_2, lon_2, alt_2 = aacgmv2.convert(60, 0, 300, dt.datetime(2013, 12, 1, 0, 0, 0))
    assert lat_1 == lat_2
    assert lon_1 == lon_2
    assert alt_1 == alt_2


def test_convert_result_values_G2A_coeff():
    lat_p, lon_p, alt_p = aacgmv2.convert(60, 0, 300, dtObj)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, alt_c = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A)
    assert lat_p == lat_c
    assert lon_p == lon_c
    assert alt_p == alt_c


def test_convert_result_values_A2G_coeff():
    lat_p, lon_p, alt_p = aacgmv2.convert(60, 0, 300, dtObj, a2g=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, alt_c = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G)
    assert lat_p == lat_c
    assert lon_p == lon_c
    assert alt_p == alt_c


def test_convert_result_values_G2A_trace():
    lat_p, lon_p, alt_p = aacgmv2.convert(60, 0, 300, dtObj, trace=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, alt_c = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, G2A | TRACE)
    assert lat_p == lat_c
    assert lon_p == lon_c
    assert alt_p == alt_c


def test_convert_result_values_A2G_trace():
    lat_p, lon_p, alt_p = aacgmv2.convert(60, 0, 300, dtObj, a2g=True, trace=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, alt_c = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, A2G | TRACE)
    assert lat_p == lat_c
    assert lon_p == lon_c
    assert alt_p == alt_c


def test_convert_result_values_allowtrace():
    lat, lon, alt = aacgmv2.convert(60, 0, [300, 5000], dtObj, allowtrace=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    np.testing.assert_allclose((lat[0], lon[0], alt[0]),
            aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, ALLOWTRACE), rtol=1e-5)
    np.testing.assert_allclose((lat[1], lon[1], alt[1]),
            aacgmv2._aacgmv2.aacgmConvert(60, 0, 5000, ALLOWTRACE), rtol=1e-5)


def test_convert_result_values_badidea():
    lat, lon, alt = aacgmv2.convert(60, 0, [300, 5000], dtObj, badidea=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    np.testing.assert_allclose((lat[0], lon[0], alt[0]),
            aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, BADIDEA), rtol=1e-5)
    np.testing.assert_allclose((lat[1], lon[1], alt[1]),
            aacgmv2._aacgmv2.aacgmConvert(60, 0, 5000, BADIDEA), rtol=1e-5)


def test_convert_result_values_geocentric():
    lat_p, lon_p, alt_p = aacgmv2.convert(60, 0, 300, dtObj, geocentric=True)
    aacgmv2._aacgmv2.setDateTime(*date)
    lat_c, lon_c, alt_c = aacgmv2._aacgmv2.aacgmConvert(60, 0, 300, GEOCENTRIC)
    assert lat_p == lat_c
    assert lon_p == lon_c
    assert alt_p == alt_c


def test_warning_below_ground():
    with pytest.warns(UserWarning):
        aacgmv2.convert(60, 0, -1, dtObj)
    with pytest.warns(UserWarning):
        aacgmv2.convert(60, 0, [300, -1], dtObj)


def test_exception_maxalt():
    with pytest.raises(ValueError):
        aacgmv2.convert(60, 0, 2001, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert(60, 0, [300, 2001], dtObj)

    # the following should not raise exceptions
    aacgmv2.convert(60, 0, 2001, dtObj, trace=True)
    aacgmv2.convert(60, 0, 2001, dtObj, allowtrace=True)
    aacgmv2.convert(60, 0, 2001, dtObj, badidea=True)


def test_exception_lat90():
    with pytest.raises(ValueError):
        aacgmv2.convert(91, 0, 300, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert(-91, 0, 300, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert([60, 91], 0, 300, dtObj)
    with pytest.raises(ValueError):
        aacgmv2.convert([60, -91], 0, 300, dtObj)

    # the following should not raise exceptions
    aacgmv2.convert(90, 0, 300, dtObj)
    aacgmv2.convert(-90, 0, 300, dtObj)


def test_forbidden():
    np.testing.assert_equal(aacgmv2.convert(7, 0, 0), (np.nan, np.nan, np.nan))


def test_MLT_forward_backward():
    mlon = aacgmv2.convert_mlt(12, dtObj, m2a=True)
    mlt = aacgmv2.convert_mlt(mlon, dtObj)
    np.testing.assert_allclose(mlt, 12)


def test_MLT_a2m():
    mlt = aacgmv2.convert_mlt([1, 12, 23], dt.datetime(2015, 2, 24, 14, 0, 15))
    np.testing.assert_allclose(mlt, [9.058207,  9.791541, 10.524874], rtol=1e-6)


def test_MLT_m2a():
    mlon = aacgmv2.convert_mlt([1, 12, 23], dt.datetime(2015, 2, 24, 14, 0, 15), m2a=True)
    np.testing.assert_allclose(mlon, [240.12689,  45.12689, 210.12689], rtol=1e-6)
