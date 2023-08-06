import os
import sys
from setuptools import setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'wraplite', '__version__.py')) as f:
    exec(f.read(), about)

if len(sys.argv) > 1:
    if sys.argv[1] == 'tag':
        option = 'build'
        if len(sys.argv) > 2:
            if sys.argv[2] == 'patch':
                option = 'patch'
            elif sys.argv[2] == 'minor':
                option = 'minor'
            elif sys.argv[2] == 'major':
                option = 'major'
            elif sys.argv[2] == 'release':
                option = 'release'
        if option == 'build' and 'dev' not in about['__version__']:
            raise ValueError('cannot tag a build without starting a patch, minor or major update')
        os.system('python -m bumpversion ' + option)
        os.system('git push')
        os.system('git push --tags')
        sys.exit()

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['wraplite'],
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=['pandas'],
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: SQL',
        'Topic :: Utilities'
    ],
    keywords='nosql sqlite wrapper wraplite sql'
)