from os.path import dirname, join

from setuptools import find_packages, setup

setup(
    name='fefu_admission',
    version='1.3',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['fefu_admission = fefu_admission.cli:cli']
    },
    install_requires=[
        "click~=7.1.2",
        "requests~=2.24.0",
        "beautifulsoup4~=4.9.1",
        "colorama~=0.4.3",
        "tabulate~=0.8.7",
        "setuptools~=49.2.0",
    ],
)
