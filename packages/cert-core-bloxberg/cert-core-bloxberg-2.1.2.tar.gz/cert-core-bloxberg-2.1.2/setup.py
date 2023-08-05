import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='cert-core-bloxberg',
    version='2.1.2',
    description='Blockcerts-bloxberg core models for python',
    author='info@bloxberg.org',
    tests_require=['tox'],
    url='https://github.com/crossoveranx/cert-core.git',
    license='MIT',
    author_email='info@bloxberg.org',
    long_description=long_description,
    packages=find_packages(),
    install_requires=reqs
)
