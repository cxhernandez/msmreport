from __future__ import print_function, absolute_import, division
import os
import shutil
import subprocess
import tempfile
from distutils.spawn import find_executable

MSMREPORT_BIN = find_executable('osprey')


def test_help():
    assert MSMREPORT_BIN is not None
    cwd = os.path.abspath(os.curdir)
    dirname = tempfile.mkdtemp()

    try:
        os.chdir(dirname)
        subprocess.check_call([MSMREPORT_BIN, '-h'])

    finally:
        os.chdir(cwd)
        shutil.rmtree(dirname)


def test_create():
    assert MSMREPORT_BIN is not None
    cwd = os.path.abspath(os.curdir)
    dirname = tempfile.mkdtemp()

    try:
        os.chdir(dirname)
        subprocess.check_call([MSMREPORT_BIN, 'create', '-h'])

    finally:
        os.chdir(cwd)
        shutil.rmtree(dirname)
