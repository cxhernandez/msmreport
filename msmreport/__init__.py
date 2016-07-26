import os

try:
    from jupyter_client.manager import start_new_kernel
except ImportError:
    start_new_kernel = None

try:
    from nbconvert.preprocessors import ExecutePreprocessor
    from nbconvert.exporters.export import exporter_map
except ImportError:
    ExecutePreprocessor = exporter_map = None

__name__ = 'msmreport'
__version__ = '0.1.0dev0'


def execute_nb(nb):
    kernel_name = nb.metadata.get('kernelspec', {}).get('name', 'python')
    km, kc = start_new_kernel(
        kernel_name=kernel_name,
        stderr=open(os.devnull, 'w'),
        cwd=None)
    kc.allow_stdin = False

    try:
        ep = ExecutePreprocessor(timeout=-1, kernel_name=kernel_name)
        nb, resources = ep.preprocess(nb, {'metadata': {'path': './'}})
    finally:
        kc.stop_channels()
        km.shutdown_kernel(now=True)

    return nb


def convert_nb(nb, output, fmt):
    exporter = exporter_map[fmt]()
    html, _ = exporter.from_notebook_node(nb)
    with open(output, 'w') as f:
        f.write(output + '.%s' % fmt)
