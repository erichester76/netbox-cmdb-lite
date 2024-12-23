from netbox.plugins import PluginMenuItem
from . import models

def get_dynamic_menu_items():
    """
    Generate dynamic menu items based on ObjectType.
    """
    object_types = models.ObjectType.objects.all()
    dynamic_menu_items = []
    for obj_type in object_types:
        dynamic_menu_items.append(
            PluginMenuItem(
                link=f"/plugins/cmdb-lite/generic-objects/?object_type={obj_type.id}",
                link_text=obj_type.name,
                permissions=["cmdb_lite.view_genericobject"],
            )
        )
    return dynamic_menu_items

def plugin_menu():
    """
    Return menu structure for the plugin.
    """
    base_menu_items = [
        PluginMenuItem(
            link="object_type_list",
            link_text="Object Types",
            permissions=["cmdb_lite.view_objecttype"],
        ),
        PluginMenuItem(
            link="relationship_type_list",
            link_text="Relationship Types",
            permissions=["cmbd_lite.view_relationshiptype"],
        ),
        PluginMenuItem(
            link="generic_relationship_list",
            link_text="Relationships",
            permissions=["cmbd_lite.view_genericrelationship"],
        ),
    ]
    return base_menu_items + get_dynamic_menu_items()
