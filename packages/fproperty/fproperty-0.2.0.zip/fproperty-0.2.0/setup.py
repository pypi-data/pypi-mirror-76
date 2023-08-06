from setuptools import setup
from fproperty._version import __version__

with open('README.md', 'rb') as fid:
    LONG_DESCRIPTION = fid.read().decode('utf8')

setup(
    name='fproperty',
    version=__version__,
    author='Roger D. Serwy',
    author_email='roger.serwy@gmail.com',
    url="http://github.com/serwy/fproperty",
    packages=['fproperty'],
    description='fproperty',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
