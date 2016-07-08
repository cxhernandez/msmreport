from setuptools import setup, find_packages

from msmreport import __version__, __name__


def main(**kwargs):
    setup(
        name=__name__,
        version=__version__,
        packages=find_packages(),
        include_package_data=True,
        package_data={
            'msmreport': ['assets/*.*', 'assets/templates/*.*']
        },
        zip_safe=True,
        platforms=["Linux", "Unix"],
        author="cxhernandez",
        author_email="cxh@stanford.edu",
        description="Create reports for MSMs generated using Osprey",
        license="MIT",
        entry_points={
            'console_scripts': [
                'msmreport = msmreport.cli.main:main',
            ],
        },
        **kwargs
    )


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
