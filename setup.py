from setuptools import setup, find_packages

setup(
    name='raccoon',
    version='1.2.5',
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
          'pika==0.11.2',
          'ujson==1.35',
      ],
    zip_safe=True
)