from setuptools import setup

setup(
    name='parserscript',
    version='0.1.0',
    py_modules=['parserscript'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'covid = parserscript:cli',
        ],
    },
)

