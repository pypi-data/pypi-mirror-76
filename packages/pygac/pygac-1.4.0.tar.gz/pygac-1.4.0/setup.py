#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Abhay Devasthale, Adam.Dybbroe, Martin Raspaud

# Author(s):

#   Adam.Dybbroe <a000680@c14526.ad.smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""The setup module."""

try:
    with open("./README", "r") as fd:
        long_description = fd.read()
except IOError:
    long_description = ""


from setuptools import setup
import imp
import sys
import os
from distutils.extension import Extension
from setuptools.command.build_ext import build_ext as _build_ext

version = imp.load_source('pygac.version', 'pygac/version.py')


def set_builtin(name, value):
    """Set builtin."""
    if isinstance(__builtins__, dict):
        __builtins__[name] = value
    else:
        setattr(__builtins__, name, value)


class build_ext(_build_ext):  # noqa
    """Work around to bootstrap numpy includes in to extensions.

    Copied from:
        http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
    """

    def finalize_options(self):
        """Finalize options."""
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        set_builtin('__NUMPY_SETUP__', False)
        import numpy
        self.include_dirs.append(numpy.get_include())


if __name__ == '__main__':
    version = imp.load_source('pygac.version', 'pygac/version.py')

    # Build extensions. On the development side, i.e. if the module is built
    # using the 'build_ext' or 'sdist' arguments, compile *.pyx using Cython.
    # On the user side, compile *.c files.
    use_cython = 'build_ext' in sys.argv or 'sdist' in sys.argv
    file_ext = '.pyx' if use_cython else '.c'
    extensions = [
        Extension('pygac._filter',
                  sources=['pygac/_filter' + file_ext])
    ]
    if use_cython:
        from Cython.Build import cythonize
        extensions = cythonize(extensions)

    requirements = ['docutils>=0.3',
                    'numpy>=1.8.0',
                    'pyorbital>=v0.3.2',
                    'h5py>=2.0.1',
                    'scipy>=0.8.0',
                    'python-geotiepoints>=1.1.8']
    if sys.version_info < (3, 7):
        # To parse ISO timestamps in calibration.py
        requirements.append('python-dateutil>=2.8.0')

    setup(name='pygac',
          version=version.__version__,
          description='NOAA AVHRR GAC/LAC reader and calibration',
          author='Abhay Devasthale, Martin Raspaud',
          author_email='martin.raspaud@smhi.se',
          classifiers=["Development Status :: 4 - Beta",
                       "Intended Audience :: Science/Research",
                       "License :: OSI Approved :: GNU General Public License v3 " +
                       "or later (GPLv3+)",
                       "Operating System :: OS Independent",
                       "Programming Language :: Python",
                       "Topic :: Scientific/Engineering"],
          url="https://github.com/pytroll/pygac",
          long_description=long_description,
          license='GPLv3',

          packages=['pygac'],
          package_data={'pygac': ['data/calibration.json']},
          cmdclass={'build_ext': build_ext},
          ext_modules=extensions,

          # Project should use reStructuredText, so ensure that the docutils get
          # installed or upgraded on the target machine
          install_requires=requirements,
          scripts=[os.path.join('bin', item) for item in os.listdir('bin')],
          data_files=[('etc', ['etc/pygac.cfg.template']),
                      ('gapfilled_tles', ['gapfilled_tles/TLE_noaa16.txt'])],
          test_suite="pygac.tests.suite",
          tests_require=[],
          python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
          zip_safe=False
          )
