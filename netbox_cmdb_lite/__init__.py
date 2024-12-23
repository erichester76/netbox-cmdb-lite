from netbox.plugins import PluginConfig

class NetboxCmdbLiteConfig(PluginConfig):
    name = 'netbox_cmdb_lite'
    verbose_name = 'NetBox CMDB Lite'
    description = 'A lightweight CMDB plugin for NetBox'
    version = '0.1'
    author = 'Eric Hester'
    author_email = 'hester1@clemson.edu'
    base_url = 'cmdb-lite'
    required_settings = []
    default_settings = {}

config = NetboxCmdbLiteConfig
