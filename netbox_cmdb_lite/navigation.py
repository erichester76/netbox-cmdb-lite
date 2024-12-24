from netbox.plugins import PluginMenu, PluginMenuItem

mgmt_items = [
        PluginMenuItem(
            link="plugins:netbox_cmdb_lite:genericobjecttype_list",
            link_text="Object Types",
            permissions=["cmdb_lite.view_objecttype"],
        ),
        PluginMenuItem(
            link="plugins:netbox_cmdb_lite:relationshiptype_list",
            link_text="Relationship Types",
            permissions=["cmbd_lite.view_relationshiptype"],
        ),
        PluginMenuItem(
            link="plugins:netbox_cmdb_lite:genericobject_list",
            link_text="Objects",
            permissions=["cmbd_lite.view_genericobject"],
        ),
        PluginMenuItem(
            link="plugins:netbox_cmdb_lite:genericrelationship_list",
            link_text="Relationships",
            permissions=["cmbd_lite.view_genericrelationship"],
        ),
]

# Define the top-level menu with icon
menu = PluginMenu(
    label="CMDB Lite",
    groups=(("Management", mgmt_items),),
    icon_class="mdi mdi-server",
)

