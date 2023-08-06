from setuptools import setup, find_packages

with open("README.md", 'r') as readme:
	long_description = readme.read()

setup(
	name = 'elementally',
	version = '0.4',
	author = 'David "Dawn" Estes McKnight',
	author_email = 'demcknig@ualberta.ca',
	description = 'Utility module for elementwise operations on basic Python'
	              ' sequence types',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url = 'https://github.com/dem1995/elementally',
	license = 'MIT/X11',
	packages = find_packages(),
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	python_requires='>=3.8'
)
