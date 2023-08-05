from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()
	
setup(
	long_description = long_description,
	long_description_content_type="text/markdown",
	name = 'matlablib',
	version='1.3',
	description = 'Matlab-tool suite', 
	license = 'MIT',
	author='Josh Philipson',
	author_email = 'philipson@gmail.com',
	url='https://github.com/OSHI7/matlablib',
	py_modules = ["matlablib"],
	package_dir = {'': 'src'},
	classifiers = [
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.6",
	"Programming Language :: Python :: 3.7",
	"Programming Language :: Python :: 3.8",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent"],
	install_requires = ['pandas', 'matplotlib', 'ipython'],
	)