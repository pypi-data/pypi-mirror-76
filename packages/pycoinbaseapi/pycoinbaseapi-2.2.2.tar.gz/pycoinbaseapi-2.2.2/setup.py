# coding: utf-8
import os
from setuptools import setup
import pycoinbaseapi.wallet

README = open(os.path.join(os.path.dirname(__file__), 'PYPIREADME.rst')).read()
REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                               'requirements.txt')).readlines()]

setup(
    name='pycoinbaseapi',
    version=pycoinbaseapi.wallet.__version__,
    packages=['pycoinbaseapi', 'pycoinbaseapi.wallet'],
    include_package_data=True,
    license='Apache 2.0',
    description='Coinbase API client library',
    long_description=README,
    url='https://github.com/GauthamramRavichandran/coinbase-python',
    download_url='https://github.com/GauthamramRavichandran/coinbase-python/tarball/%s' % (
        pycoinbaseapi.wallet.__version__),
    keywords=['api', 'coinbase', 'bitcoin', 'oauth2', 'client'],
    install_requires=REQUIREMENTS,
    author='Gauthamram Ravichandran',
    author_email='api@coinbase.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
