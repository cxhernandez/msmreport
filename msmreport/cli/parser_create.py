from __future__ import print_function, absolute_import, division
from argparse import ArgumentDefaultsHelpFormatter

from nbconvert.exporters.export import exporter_map


def func(args, parser):
    # delay import of the rest of the module to improve `osprey -h` performance
    from os.path import splitext, basename
    from .. import execute_nb, convert_nb
    from ..utils import Timing, nb_template

    yaml, tmp, fmt = args.yaml, args.tmp, args.fmt

    output = basename(splitext(yaml)[0])
    with Timing('reading osprey config...'):
        nb = nb_template(yaml, tmp=tmp)
    with Timing('generating report...'):
        nb = execute_nb(nb)
    with Timing('saving as %s...' % fmt):
        convert_nb(nb, output, fmt)


def configure_parser(sub_parsers):
    help = 'Generate a report for an MSM made with osprey'
    p = sub_parsers.add_parser('create', description=help, help=help,
                               formatter_class=ArgumentDefaultsHelpFormatter)
    p.add_argument('-y', '--yaml', dest='yaml',
                   help='Path to Osprey config file')
    p.add_argument('-t', '--template', dest='tmp',
                   default=None,
                   help='Path to ipynb')
    p.add_argument('-f', '--format', dest='fmt',
                   choices=exporter_map.keys(),
                   default='html',
                   help='Output file format')
    p.set_defaults(func=func)
