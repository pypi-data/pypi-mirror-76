from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='uspspy',
    version='0.0.2',
    description='Validate addresses with the USPS API.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://poplars.dev',
    author='Chris Binckly, Poplar Development',
    author_email='chris@poplars.dev',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    keywords='USPS Address Validation API XML',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    package_data={
    },
)

