# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from codecs import open  # To use a consistent encoding
from os import path

from setuptools import setup

HERE = path.dirname(path.abspath(__file__))

# Get version info
ABOUT = {}
with open(path.join(HERE, 'stackstate_checks', 'kubernetes_state', '__about__.py')) as f:
    exec(f.read(), ABOUT)

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Parse requirements
def get_requirements(fpath):
    with open(path.join(HERE, fpath), encoding='utf-8') as f:
        return f.readlines()


CHECKS_BASE_REQ = 'stackstate-checks-base'

setup(
    name='stackstate-kubernetes_state',
    version=ABOUT['__version__'],
    description='The Kubernetes State check',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='stackstate agent kubernetes_state check',
    # The project's main homepage.
    url='https://github.com/StackVista/stackstate-agent-integrations',
    # Author details
    author='StackState',
    author_email='info@stackstate.com',
    # License
    license='BSD',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    # The package we're going to ship
    packages=['stackstate_checks.kubernetes_state'],
    # Run-time dependencies
    install_requires=[CHECKS_BASE_REQ],
    # Extra files to ship with the wheel package
    include_package_data=True,
)
