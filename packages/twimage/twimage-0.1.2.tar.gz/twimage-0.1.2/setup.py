from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='twimage',
    version='0.1.2',
    license='MIT',
    py_modules=['twimage'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        twimage=twimage:cli
    ''',
    long_description=long_description,
    long_description_content_type='text/markdown',
)