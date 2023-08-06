from setuptools import setup
version='0.0.0'
name='object_compresser'
with open('README.md', 'r') as f:
	readme=f.read()
setup(
name=name,
version=version,
author='bhanu',
author_email='bhanuponguru@gmail.com',
url='https://github.com/bhanuponguru/' + name + '.git',
description='this is just a symple module to save/load data to/from your file.',
long_description=readme,
long_description_content_type="text/markdown",
packages=[name]
)