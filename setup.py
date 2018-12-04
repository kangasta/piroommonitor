#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="piroommonitor",
	version="0.1.1",
	author="Toni Kangas",
	description="Room monitor for reading data from sensors and pushing it forward",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kangasta/piroommonitor",
	packages=setuptools.find_packages(),
	scripts=["bin/piroommonitor"],
	install_requires=[
		"fdbk",
		"adafruit-bmp",
		"fdbk",
		"pi_si7021",
		"tsl2561"
	],
	classifiers=(
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	)
)
