from setuptools import setup,find_packages
setup(
    name='blade_runner',
    include_package_data=True,
    version='1.0.8',
    packages=find_packages(),
    package_data={'blade_runner': ['blade_runner'],},
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['pygame'],
)