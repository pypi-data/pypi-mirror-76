from distutils.core import setup
import setuptools

setup(
    name='data_etl',
    version='0.1.3dev',
    packages=['data_etl',],
    license='MIT',
    url="https://github.com/gigisr/data_etl",
    install_requires=[
          'pandas', 'numpy', 'pyodbc'
      ],
    
    author='GigiSR'
)
