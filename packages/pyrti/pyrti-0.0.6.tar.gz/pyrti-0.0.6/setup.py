from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pyrti',
    version='0.0.6',
    url='https://github.com/infopontes/rti',
    license='MIT License',
    author='Marcelo Pontes Rodrigues',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='infopontes@gmail.com',
    keywords='Package, RT, Python',
    description=u'RTIntegration (rti) - Python interface to Request Tracker API REST 2.0',
    packages=['pyrti'],
    install_requires=['requests'],)