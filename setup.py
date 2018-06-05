from setuptools import setup, find_packages

setup(
    name='house-price-calculator',
    version='1.1',
    packages=find_packages(exclude=['tests*']),
    setup_requires=['setuptools-git'],
    license='MIT',
    description='Library designed for calculating house prices.',
    long_description=open('README.md').read(),
    install_requires=['googlemaps'],
    url='https://git.e-science.pl/kcieslik226138/house_price_calculator_library',
    author='Kamil Cieslik',
    author_email='mrfarinq@hotmail.com'
)
