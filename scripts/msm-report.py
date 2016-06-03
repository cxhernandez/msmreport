#! /usr/bin/env python

import argparse

from os.path import splitext, basename

from nbconvert.exporters.export import exporter_map

from msmreport import execute_nb, convert_nb
from msmreport.utils import Timing, nb_template


def run(yaml, fmt):
    output = basename(splitext(yaml)[0])
    with Timing('reading osprey config...'):
        nb = nb_template(yaml)
    with Timing('generating report...'):
        nb = execute_nb(nb)
    with Timing('saving as %s...' % fmt):
        convert_nb(nb, output, fmt)


def parse_cmdln():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-y', '--yaml', dest='yaml',
                        help='Path to Osprey config file')
    parser.add_argument('-f', '--format', dest='fmt',
                        choices=exporter_map.keys(),
                        default='html',
                        help='Path to Osprey config file')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    options = parse_cmdln()
    run(options.yaml, options.fmt)
