#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='aquarius_time',
	version='0.1.0',
	packages=find_packages(),
	scripts=['bin/aq'],
	description='Scientific time library for Python',
	author='Peter Kuma',
	author_email='peter@peterkuma.net',
	license='MIT',
	keywords=['time', 'date', 'julian-date', 'datetime', 'utc', 'tai', 'iso-8601'],
	url='https://github.com/peterkuma/aquarius-time',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries',
		'Topic :: Scientific/Engineering',
	],
)
