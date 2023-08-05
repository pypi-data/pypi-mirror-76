from setuptools import setup,find_packages
setup(
    name='blade_runner',
    version='1.0.1',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['pygame'],
    package_data={'':['*.png','*.pxe','*.wav']}
)