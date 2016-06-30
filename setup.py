#!/usr/bin/env python

PROJECT = 'Phenopacket-scraper'


VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='CLI for phenopacket-scraper core',
    long_description=long_description,

    author='Satwik Bhattamishra',
    author_email='satwik55@gmail.com',

    url='https://github.com/monarch-initiative/phenopacket-scraper-core',

    classifiers=[
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'beautifulsoup4', 'requests', 'html2text'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'pps = pps.main:main'
        ],
        'pps_commands': [
            'scrape = pps.scraper:Scraper',
            'annotate = pps.scraper:Annotate',
            'phenopacket = pps.phenopacket:GenPhenoPacket',         
            'error = pps.scraper:Error',
        ],
    },

    zip_safe=False,
)
