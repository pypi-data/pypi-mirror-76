from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'aiostp/version.py').load_module()

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='aiostp',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='asyncio client library for stpmex.com',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/cuenca-mx/aiostp',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(stpmex=['py.typed']),
    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3.6.2,<3.7.0',
        'cryptography>=3.0,<4.1',
        'cuenca-validations>=0.4.1,<0.6.0',
    ],
    setup_requires=['pytest-runner'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
