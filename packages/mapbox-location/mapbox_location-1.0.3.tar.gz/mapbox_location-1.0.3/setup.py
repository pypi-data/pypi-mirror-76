from setuptools import setup, find_packages

with open('mapbox_location/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

setup(
    name='mapbox_location',
    version=version,
    description='draw mapbox location',
    url='https://github.com/whatever/whatever',
    author='iwata_n',
    author_email='a.tokai.wain@gmail.com',
    license='MIT',
    keywords='mapbox',
    packages=find_packages(exclude=['test']),
    package_data={
        'mapbox_location': ['templates/*']},
    install_requires=['mapboxgl'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)