from setuptools import setup

setup(
    name='Resultor',
    version='0.0.1',
    py_modules=['resultor'],
    entry_points={
        'nose.plugins.0.10': [
            'Resultor = resultor:Resultor'
        ]
    },
)