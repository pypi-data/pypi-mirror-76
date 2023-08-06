from setuptools import setup
from os import path
import io

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py2ipynb',
    packages=['ipynb_py_convert'],
    version='0.0.1',
    description='Convert .py files runnable in VSCode/Python or Atom/Hydrogen to jupyter .ipynb notebooks and vice versa',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Noj Vek',
    author_email='graykode@gmail.com',
    license='MIT',
    url='',
    keywords=['vscode', 'jupyter', 'convert', 'ipynb', 'py', 'atom', 'hydrogen'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'ipynb-py-convert=ipynb_py_convert.__main__:main',
        ],
    },
)
