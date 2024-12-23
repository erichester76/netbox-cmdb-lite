from setuptools import find_packages, setup

setup(
    name='netbox-cmdb-lite',
    version='0.1',
    description='A lightweight CMDB plugin for NetBox',
    url='https://github.com/clemson-netbox/netbox-cmdb-lite',
    author='Eric Hester',
    author_email='hester1@clemson.edu',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'django_tables2',
    ],
    include_package_data=True,
    package_data={
        '': ['LICENSE'],
    },
    zip_safe=False,
 
)
