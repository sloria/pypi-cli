import sys
import re
import subprocess

from setuptools import setup
from setuptools.command.test import test as TestCommand

REQUIRES = [
    'requests>=2.3.0',
    'python-dateutil==2.2',
    'click==2.0'
]

TESTS_REQUIRE = [
    'pytest',
    'responses'
]

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("pypi_cli.py")

PUBLISH_CMD = "python setup.py register sdist upload"
TEST_PUBLISH_CMD = 'python setup.py register -r test sdist upload -r test'

if 'publish' in sys.argv:
    status = subprocess.call(PUBLISH_CMD, shell=True)
    sys.exit(status)

if 'publish_test' in sys.argv:
    status = subprocess.call(TEST_PUBLISH_CMD, shell=True)
    sys.exit()

def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='pypi-cli',
    version=__version__,
    description='A CLI for getting PyPI package info and metrics',
    long_description=(read("README.rst") + '\n\n' +
                      read('HISTORY.rst')),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/pypi-cli',
    install_requires=REQUIRES,
    license=read("LICENSE"),
    zip_safe=False,
    keywords='pypi cli command line pipstat pip statistics download count metrics analytics',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    py_modules=["pypi_cli"],
    entry_points={
        'console_scripts': [
            "pypi = pypi_cli:cli"
        ]
    },
    tests_require=TESTS_REQUIRE,
    cmdclass={'test': PyTest}
)
