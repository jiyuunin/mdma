import codecs
import os
import re

from setuptools import find_packages, setup


def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'rb', 'utf-8') as f:
        return f.read()


def find_version(*file_paths):
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='mdma',
    version=find_version('mdma', '__init__.py'),
    description='Moe\'s Dynamic Maker Awards The Game.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    author='jiyuunin',
    author_email='jiyuunin@protonmail.com',
    packages=find_packages(exclude=['tests*']),
    package_data={'mdma': ['config.yml', 'fonts/*', 'graphics/*']},
    install_requires=[
        'pygame',
        'pyyaml'
    ],
    entry_points={
        'gui_scripts': [
            'mdma = mdma.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
    ],
)
