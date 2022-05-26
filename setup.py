from setuptools import setup, find_packages

import versioneer

setup(
    name='raccoon',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
    install_requires=[
        'pika==0.12.0',
        'ujson==5.2.0'
    ],
    zip_safe=True
)
