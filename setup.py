from setuptools import setup, find_packages
import pip


requirements_file = 'requirements.txt'
INSTALL_REQUIRES = [req.name for req in pip.req.parse_requirements(requirements_file, session='hack')]

setup(
    name='raccoon',
    version='1.0.0',
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
          'numpydoc',  # necessary for Sphinx to understand Numpy-style docstrings
          INSTALL_REQUIRES,
      ],
    zip_safe=True
)