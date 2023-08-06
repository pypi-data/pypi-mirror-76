from setuptools import find_packages, setup

setup(
    name='vespa-plugin',
    version='0.1',
    description='An useless NetBox plugin',
    url='https://github.com/lvrfrc87/netbox_vespa_plugin',
    author='Federico Olivieri',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)
