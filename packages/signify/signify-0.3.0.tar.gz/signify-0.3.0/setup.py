import glob
import os
from setuptools import setup


base_dir = os.path.dirname(__file__)
about = {}
with open(os.path.join(base_dir, "signify", "__init__.py")) as f:
    exec(f.read(), about)

try:
    long_description = open("README.rst", "r").read()
except Exception:
    long_description = None


setup(
    name='signify',
    version=about['__version__'],
    packages=['signify', 'signify.asn1'],
    package_data={'signify': ['*.pem']},
    include_package_data=True,

    url='https://github.com/ralphje/signify',
    download_url='https://github.com/ralphje/signify/tarball/v' + about['__version__'],
    license='MIT',
    author='Ralph Broenink',
    author_email='ralph@ralphbroenink.net',
    description='Module to generate and verify PE signatures',
    long_description=long_description,
    install_requires=['pyasn1>=0.4.0', 'certvalidator>=0.11', 'asn1crypto', 'oscrypto', 'pyasn1-modules'],
    extras_require={
        "stlupdate": ["requests"],
    },
    keywords=['authenticode', 'authentihash', 'fingerprinter', 'pe'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Security :: Cryptography',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ],
)
