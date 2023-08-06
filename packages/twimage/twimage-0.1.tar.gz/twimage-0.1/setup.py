from setuptools import setup, find_packages

setup(
    name='twimage',
    version='0.1',
    license='MIT',
    py_modules=['twimage'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        twimage=twimage:cli
    ''',
)