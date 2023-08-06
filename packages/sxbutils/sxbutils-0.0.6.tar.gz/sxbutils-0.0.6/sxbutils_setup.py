"""Setup for the sxbutils package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Steve Botham",
    author_email="sbotham1968@gmail.com",
    name='sxbutils',
    license="MIT",
    description='Some utilities.',
    version='0.0.6',
    long_description=README,
    url='https://github.com/shaypal5/chocobo',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
