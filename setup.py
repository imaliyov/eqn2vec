from setuptools import setup, find_packages

setup(
    name='eqn2vec',
    version='0.0.1',
    author='Ivan Maliyov',
    author_email='ivan.maliyov@gmail.com',
    description='Convert latex equations to vector image files',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
    'latex',
    ],
)
