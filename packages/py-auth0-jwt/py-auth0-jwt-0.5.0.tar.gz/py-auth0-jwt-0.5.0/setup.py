from distutils.core import setup
from setuptools import find_packages

setup(
    name='py-auth0-jwt',
    version='0.5.0',
    packages=['pyauth0jwt',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=["jwcrypto", "cryptography", "furl", "pyjwt", "requests", "Django>=1.11"],
)
