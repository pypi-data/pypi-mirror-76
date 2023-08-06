from setuptools import find_packages, setup
setup(
    name='chosendata',
    version='1.0.1',
    description='a data and model tools',
    author='chosendata',
    author_email='jiuxindata@163.com',
    url='http://www.chosen-data.com/',
    packages=find_packages(),
    install_requires=['requests', 'pandas', 'numpy', 'xlrd', 'xlutils'],
)