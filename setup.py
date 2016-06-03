from setuptools import setup, find_packages

from glob import glob

setup(
    name="msmreport",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'msmreport': ['assets/*.*', 'assets/templates/*.*']
    },
    scripts=glob('./scripts/*.py'),
    zip_safe=True,
    platforms=["Linux", "Unix"],
    author="cxhernandez",
    author_email="cxh@stanford.edu",
    description="Create reports for MSMs generated using Osprey",
    license="MIT",
)
