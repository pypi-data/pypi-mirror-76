import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
test_suffix = '-noahgill409'

IS_TEST = False
package_name = 'bedevere'

if IS_TEST:
	name = ''.join([package_name, test_suffix])

else:
	name = package_name


setuptools.setup(
	name=name,
	version='0.1.1',
	author='noahgill409',
	author_email='noahgill409@gmail.com',
	description='A collection of useful mathematical functions for my other projects',
	long_description=README,
	long_description_content_type='text/markdown',
	url=r'https://github.com/noahgill409/bedevere',
	packages=setuptools.find_packages(),
	install_requires=['numpy'],
	license='MIT',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
	],

	include_package_data=True,
)
