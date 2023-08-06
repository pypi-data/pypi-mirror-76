#from distutils.core import setup
from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()

setup(
    name='fasta_manipulate_scripts',
    version='1.0.0',
    description=readme(),
    author='wison',
    author_email='15527825168@163.com',
    py_modules=["packages_1.function_1","packages_1.function_2"])

