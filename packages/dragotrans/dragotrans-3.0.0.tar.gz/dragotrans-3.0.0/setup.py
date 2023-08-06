#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re

from setuptools import setup, find_packages


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def get_version():
    init_py = get_file(os.path.dirname(__file__), 'dragotrans', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def get_description():
    init_py = get_file(os.path.dirname(__file__), 'dragotrans', '__init__.py')
    pattern = r'"""(.*?)"""'
    description, = re.findall(pattern, init_py, re.DOTALL)
    return description


def get_readme():
    return get_file(os.path.dirname(__file__), 'README.rst')


def install():
    setup(
        name='dragotrans',
        version=get_version(),
        description=get_description(),
        long_description=get_readme(),
        license='MIT',
        author='Emerger',
        author_email='sumitkhamar22@gmail.com',
        url='https://github.com/sumitkhamar22/dragotrans',
        download_url='https://github.com/sumitkhamar22/dragotrans/archive/0.0.1.tar.gz',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Education',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Education',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8'],
        packages=find_packages(exclude=['docs', 'tests']),
        keywords='google translate translator',
        install_requires=[
            'httpx==0.13.3',
        ],
        python_requires= '>=3.6',
        tests_require=[
            'pytest',
            'coveralls',
        ],
        scripts=['translate']
    )


if __name__ == "__main__":
    install()
