from bestiary_loader import BESTIARY_DATA, NATURES

def retrieve_natures():
    return { nature_properties.get('name'): nature_properties.get('creatures') for nature_properties in NATURES.values() }

def retrieve_creature(creature_key):
    return BESTIARY_DATA.get(creature_key)