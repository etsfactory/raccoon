from setuptools import setup, find_packages

from version import __version__


with open('requirements.txt') as fp:
    install_requires = fp.read()


setup(
    name='raccoon',
    version=__version__,
    description='Library that is a wrapper over pika, a python library that interacts with rabbitmq ',
    author='ETS',
    packages=find_packages(exclude=['tests', 'docs']),
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=install_requires,
    zip_safe=True
)
