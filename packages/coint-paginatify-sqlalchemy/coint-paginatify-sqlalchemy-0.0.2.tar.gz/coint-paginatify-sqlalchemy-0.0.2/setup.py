from setuptools import setup

setup(
    name='coint-paginatify-sqlalchemy',
    version='0.0.2',
    packages=['paginatify_sqlalchemy'],
    zip_safe=False,
    install_requires=['coint-paginatify==0.0.5', 'sqlalchemy>=1.0.11']
)
