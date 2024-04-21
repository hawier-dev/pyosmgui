from setuptools import setup, find_packages

setup(
    name='pyosmgui',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "geocoder"
    ],
    author='Mikołaj Badyl',
    author_email='mikolajbadyl0@gmail.com',
    description='Widget for PySide6 to display OpenStreetMap',
    license='MIT',
    keywords='osm openstreetmap gui',
    url='https://github.com/hawier-dev/pyosmgui'
)
