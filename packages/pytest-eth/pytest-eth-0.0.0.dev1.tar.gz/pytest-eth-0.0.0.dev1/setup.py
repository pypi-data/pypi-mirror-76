from setuptools import setup
import os

# with open("README.md", "r") as readme:
#     long_description = readme.read()

setup(
    name="pytest-eth",
    version='0.0.0.dev1',
    description='PyTest plugin for testing Smart Contracts for Ethereum Virtual Machine (EVM).',
    long_description='long_description',
    long_description_content_type="text/markdown",
    license='MIT',
    author='Meheret Tesfaye',
    author_email='meherett@zoho.com',
    url='https://github.com/meherett/pytest-eth',
    python_requires='>=3.6,<4',
    packages=['pytest_eth'],
    entry_points={
        'pytest11': [
            'name_of_plugin = pytest_eth',
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Framework :: Pytest",
    ],
)
