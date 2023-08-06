
Changelog
=========
2.6.0 (2020-08-16)
-----------------------------------------
* Same as 2.6.0-rc2


2.6.0-rc2 (2020-08-14)
-----------------------------------------
* Binary wheels for MacOSX


2.6.0-rc1 (2020-08-12)
-----------------------------------------
* Updated AACGM-v2 coefficients derived using the IGRF13 model
* Updated IGRF and GUFM1 coefficients using the IGRF13 model
* Added additional checks to the C code for reading the IGRF13 coefficient file
* Updated CI setup on travis and appveyor
* Deployment of linux and osx wheels to the package index
* Changed version support to 2.7, 3.4, 3.5, 3.6, 3.7, and 3.8
* Updated test values to match new coefficients


2.5.0 (unreleased)
-----------------------------------------
* Updated C code and coefficients to version 2.5.


2.3.9 (2018-05-27)
-----------------------------------------

* Update to AACGM-v2.4, which includes changes to the inverse MLT and
  dipole tilt functions and some minor bug fixes
* Updated dependencies
* Removed support for python 3.3


2.0.0 (2016-11-03)
-----------------------------------------

* Change method of calculating MLT, see documentation of convert_mlt for details


1.0.13 (2015-10-30)
-----------------------------------------

* Correctly convert output of subsol() to geodetic coordinates (the error in MLT/mlon conversion was not large, typically two decimal places and below)


1.0.12 (2015-10-26)
-----------------------------------------

* Return nan in forbidden region instead of throwing exception


1.0.11 (2015-10-26)
-----------------------------------------

* Fix bug in subsolar/MLT conversion


1.0.10 (2015-10-08)
-----------------------------------------

* No code changes, debugged automatic build/upload process and needed new version numbers along the way


1.0.0 (2015-10-07)
-----------------------------------------

* Initial release
