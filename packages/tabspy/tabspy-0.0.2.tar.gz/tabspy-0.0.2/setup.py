from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tabspy',
    version='0.0.2',
    description='TABSPY by SB',
    install_requires=['numpy',],
    py_modules=['tabspy.utils', 'tabspy.strategy.strategy'],
    license='The MIT License (MIT)',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tabspy',
)