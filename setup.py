from setuptools import setup

setup(
    name='Resultor',
    version='0.0.2',
    py_modules=['resultor'],
    entry_points={
        'nose.plugins.0.10': [
            'Resultor = resultor:Resultor'
        ]
    },
)
