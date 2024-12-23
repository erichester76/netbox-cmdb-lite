from setuptools import find_packages, setup

setup(
    name='netbox_cmdb_lite',
    version='0.1',
    description='A lightweight CMDB plugin for NetBox',
    url='https://github.com/clemson-netbox/netbox_cmdb_lite',
    author='Eric Hester',
    author_email='hester1@clemson.edu',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'django_tables2',
    ],
    include_package_data=True,
    zip_safe=False,
)
