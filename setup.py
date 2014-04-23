from setuptools import setup

setup(
    name='Resultor',
    version='0.0.3',
    description='Plugin to send test result to resultor',
    author='Daniel Anggrianto',
    author_email='daniela@aweber.com',
    py_modules=['resultor'],
    entry_points={
        'nose.plugins.0.10': [
            'Resultor = resultor:Resultor'
        ]
    },
)
