from bestiary_loader import BESTIARY_DATA, NATURES

def retrieve_natures():
    return { nature_properties.get('name'): nature_properties.get('beasts') for nature_properties in NATURES.values() }

def retrieve_beast(beast_key):
    return BESTIARY_DATA.get(beast_key)