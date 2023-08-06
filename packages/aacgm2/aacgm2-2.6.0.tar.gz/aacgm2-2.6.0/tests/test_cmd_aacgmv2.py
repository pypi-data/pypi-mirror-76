# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

import os
import subprocess

import numpy as np


def setup_function(function):
    try:
        os.remove('tests/output.txt')
    except:
        pass

teardown_function = setup_function


def test_module_invocation():
    p = subprocess.Popen(['python', '-m', 'aacgm2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data,
            [[57.4810, 93.5290, 1.04566],
             [58.5380, 93.9324, 1.0456],
             [59.5900, 94.3614, 1.04556]], rtol=1e-4)


def test_convert_g2a():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data,
            [[57.4810, 93.5290, 1.04566],
             [58.5380, 93.9324, 1.0456],
             [59.5900, 94.3614, 1.04556]], rtol=1e-4)


def test_convert_a2g():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-v'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data,
            [[51.6616, -66.6338, 306.1783],
             [52.6792, -66.7291, 306.5470],
             [53.6980, -66.8286, 306.91265]], rtol=1e-4)


def test_convert_trace_g2a():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-t'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data,
            [[57.4785, 93.5398, 1.04566],
             [58.5354, 93.9438, 1.04561],
             [59.5873, 94.3731, 1.04556]], rtol=1e-4)


def test_convert_trace_a2g():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-t', '-v'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data,
            [[51.6524, -66.6180, 306.1750],
             [52.6738, -66.7167, 306.5451],
             [53.6964, -66.8202, 306.9121]], rtol=1e-4)


def test_convert_geocentric():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-g'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data,
            [[57.6746, 93.6036, 1.0471],
             [58.7271, 94.0102, 1.0471],
             [59.7743, 94.4425, 1.0471]], rtol=1e-4)


def test_convert_today():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert.txt'])
    p.communicate()
    p.wait()


def test_convert_single_line():
    p = subprocess.Popen(['aacgm2', 'convert', '-i', 'tests/test_convert_single_line.txt',
                          '-d', '20150224', '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [57.4810, 93.5290, 1.04566], rtol=1e-4)


def test_convert_stdin_stdout():
    p = subprocess.Popen('echo 60 15 300 | aacgm2 convert -d 20150224', shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    p.wait()
    assert b'57.48099198 93.52895314 1.04566346' in stdout


def test_convert_mlt_a2m():
    p = subprocess.Popen(['aacgm2', 'convert_mlt', '-i', 'tests/test_convert_mlt.txt',
                          '20150224140015', '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [9.058207,  9.791541, 10.524874], rtol=1e-6)


def test_convert_mlt_m2a():
    p = subprocess.Popen(['aacgm2', 'convert_mlt', '-i', 'tests/test_convert_mlt.txt',
                          '20150224140015', '-o', 'tests/output.txt', '-v'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [240.12689,  45.12689, 210.12689], rtol=1e-6)


def test_convert_mlt_single_line():
    p = subprocess.Popen(['aacgm2', 'convert_mlt', '-i', 'tests/test_convert_mlt_single_line.txt',
                          '20150224140015', '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, 9.058207, rtol=1e-6)


def test_convert_mlt_stdin_stdout():
    p = subprocess.Popen('echo 12 | aacgm2 convert_mlt -v 20150224140015', shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    p.wait()
    assert b'45.12689024' in stdout


def test_convert_mlt_stdin_stdout_order():
    p = subprocess.Popen('echo 12 | aacgm2 convert_mlt 20150224140015 -v', shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    p.wait()
    assert b'45.12689024' in stdout
