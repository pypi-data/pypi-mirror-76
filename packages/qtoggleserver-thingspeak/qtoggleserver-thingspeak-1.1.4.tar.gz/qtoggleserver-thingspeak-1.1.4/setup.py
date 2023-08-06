
from setuptools import setup, find_namespace_packages


setup(
    name='qtoggleserver-thingspeak',
    version='1.1.4',
    description='Send values from qToggleServer to ThingSpeak',
    author='Calin Crisan',
    author_email='ccrisan@gmail.com',
    license='Apache 2.0',

    packages=find_namespace_packages(),

    install_requires=[
        'aiohttp'
    ]
)
