from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='rti',
    version='0.0.3',
    url='https://github.com/infopontes/rti',
    license='MIT License',
    author='Marcelo Pontes Rodrigues',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='infopontes@gmail.com',
    keywords='Pacote',
    description=u'Pacote para integração do Request Tracker RT no PyPI',
    packages=['python-rti'],
    install_requires=['requests'],)