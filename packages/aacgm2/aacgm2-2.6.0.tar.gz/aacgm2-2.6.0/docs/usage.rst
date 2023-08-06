==============
Usage examples
==============

Python library
==============

For full documentation of the functions, see :doc:`Reference → aacgm2 <reference/aacgmv2>`.

  >>> from aacgm2 import convert
  >>> from datetime import date
  >>> # geo to AACGM, single numbers
  >>> mlat, mlon, malt = convert(60, 15, 300, date(2013, 11, 3))
  >>> "{0:.8f}".format(float(mlat))
  '57.47357891'
  >>> "{0:.8f}".format(float(mlon))
  '93.61113360'
  >>> "{0:.8f}".format(float(malt))
  '1.04566346'
  >>> # AACGM to geo, mix arrays/numbers
  >>> glat, glon, galt = convert([90, -90], 0, 0, date(2013, 11, 3), a2g=True)
  >>> ["{0:.8f}".format(float(gl)) for gl in glat]
  ['82.96859922', '-74.33899667']
  >>> ["{0:.8f}".format(float(gl)) for gl in glon]
  ['-84.65010944', '125.84759847']
  >>> ["{0:.8f}".format(float(ga)) for ga in galt]
  ['14.12457922', '12.87721946']




Command-line interface
======================

.. highlight:: none

The Python package also installs a command called ``aacgm2`` with two sub-commands, ``aacgm2 convert`` and ``aacgm2 convert_mlt``. The command-line interface allows you to make use of the Python library even if you don't know or use Python. See :doc:`Reference → Command-line interface <reference/cli>` for a list of arguments to the commands. Below are some simple usage examples.


Convert geographical/magnetic coordinates
-----------------------------------------

Produce a file called e.g. ``input.txt`` with the input latitudes, longitudes and altitudes on each row separated by whitespace::

    # lat lon alt
    # comment lines like these are ignored
    60 15 300
    61 15 300
    62 15 300

To convert this to AACGM-v2 for the date 2015-02-24, run the command ``aacgm2 convert -i input.txt -o output.txt -d 20150224``. The output file will look like this::

    57.47612194 93.55719875
    58.53323704 93.96069212
    59.58522105 94.38968625

Alternatively, you can skip the files and just use command-line piping::

    $ echo 60 15 300 | aacgm2 convert -d 20150224
    57.47612194 93.55719875


Convert MLT
-----------

This works in much the same way as ``convert``. The file should only contain a single column of numbers (MLTs or magnetic longitudes, depending on which way you're converting)::

    1
    12
    23

To convert these MLTs to magnetic longitudes at 2015-02-24 14:00:15, run e.g. ``aacgm2 convert_mlt 20150224140015 -i input.txt -o output.txt -v`` (note that the date/time is a required parameter). The output file will then look like this::

    240.13651777
    45.13651777
    210.13651777

Like with ``convert``, you can use stdin/stdout instead of input/output files::

    $ echo 12 | aacgm2 convert_mlt 20150224140015 -v
    45.13651777
