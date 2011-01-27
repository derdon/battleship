import sys

from setuptools import setup

if sys.version_info < (2, 5):
    sys.exit(
        "Fatal Error: couldn't install battleship. Reason: Python version is "
        "too low (Python2.5 or higher is required)")

# copied from
# http://lucumr.pocoo.org/2010/2/11/porting-to-python-3-a-guide/
extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
        use_2to3_fixers=['custom_fixers'])

requirements = ['asynchia', 'distribute']

setup(
    name='battleship',
    description='a battleship game with a curses interface',
    long_description='',
    version='0.1a',
    author='Simon Liedtke',
    author_email='liedtke.simon@googlemail.com',
    url='http://pypi.python.org/pypi/battleship',
    license='WTFPL',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment'],
    **extra
)

