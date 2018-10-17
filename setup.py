from setuptools import find_packages, setup
from nselec import __version__ as nselec_version

setup(
    name='nselec',
    version=nselec_version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'tinydb',
        'tinydb-serialization',
        'ago',
    ],
)
