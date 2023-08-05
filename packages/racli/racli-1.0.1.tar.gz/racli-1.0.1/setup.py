from setuptools import setup

setup(
    name='racli',
    version='1.0.1',
    py_modules=['racli'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        racli=racli.racli:cli
    ''',
)