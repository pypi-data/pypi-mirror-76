"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup
import pathlib

long_description = (pathlib.Path(__file__).parent.resolve() / 'README.rst').read_text(encoding='utf-8')

setup(
    name='apispec-py35-compat',
    version='1.0.0',
    description='Python 3.5 compat package for apispec',
    long_description=long_description,
    url='https://github.com/theirix/apispec-py35-compat',
    author='theirix',
    author_email='theirix@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    install_requires=['apispec'],
    packages=['apispec'],
    python_requires='>=3.5, <4',
)
