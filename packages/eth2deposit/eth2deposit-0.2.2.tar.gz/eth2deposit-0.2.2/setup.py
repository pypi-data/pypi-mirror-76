from setuptools import find_packages, setup

"""
THIS IS A STUB FOR RUNNING THE APP
"""

setup(
    name="eth2deposit",
    version='0.2.2',
    py_modules=["eth2deposit"],
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires=">=3.7,<4",
    install_requires=[
      'click==7.0',
      'eth-typing==2.2.1',
      'pycryptodome==3.9.7',
      'py-ecc==4.0.0',
      'ssz==0.2.3',
    ]
)
