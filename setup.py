
# TODO: WIP

from setuptools import setup

setup(
    name='Automated collection of multi-source spatial information for emergency management',
    version='0.1.0',
    author='Sandra Moen',
    author_email='sandramoen01@gmail.com',
    packages=['Frontend', 'Backend'],
    scripts=[],
    url='https://github.com/Slideshow776/DATMAS-V18#datmas-v18',
    license='LICENSE.txt',
    description='W python version 3.6.4',
    long_description=open('README.md').read(),
    install_requires=[
        "Pillow==5.0.0",
        "numpy==1.22.0",
		"matplotlib==2.1.2",
		"openpyxl==2.4.10",
		"twitter==1.18.0",
        "polyline==1.3.2"
    ],
)
