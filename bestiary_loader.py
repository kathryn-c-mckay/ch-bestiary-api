import os
import json
import re
from collections.abc import Iterable
from numbers import Number

def fix_description(description):
    if isinstance(description, str):
        description = re.sub(r'(\[|\]\(.*?\))', '', description)
        description = re.sub(r'\n{1,}', '<p>',description)
        return description
    elif isinstance(description, dict):
        return { k: fix_description(v) for k,v in description.items() }
    elif isinstance(description, Iterable):
        return [ fix_description(x) for x in description ]
    elif isinstance(description, Number):
        return description
    raise TypeError(type(description))

BASE_DIR = os.path.dirname(__file__)
CREATURE_DATA_KEYS = ['name', 'rank', 'nature', 'features', 'drives', 'tactics', 'description']
BESTIARY_DATA = {}
NATURES = {}
RANKS = {1: 'Troublesome', 2: 'Dangerous', 3: 'Formidable', 4: 'Extreme', 5: 'Epic'}
for path in ['datasworn/classic/classic.json', 'datasworn/delve/delve.json']:
    with open(os.path.join(BASE_DIR, path), 'r', encoding='utf-8') as f:
        npc_list = json.load(f).get('npcs', [])
    for nature_key, nature_properties in npc_list.items():
        # Read in creatures from this source book. E.g.
        #  { ...
        #      'iron-wracked-beast': {
        #          'name': 'Iron-Wracked Beast',
        #          'rank': ...,
        #          'nature': 'beast',
        #       }
        #  }
        creature_collection = { orig_creature_key.replace('_', '-'): creature_properties for orig_creature_key, creature_properties in nature_properties.get('contents', {}).items() }
        for creature in creature_collection.values():
            creature['rank'] = RANKS[creature['rank']]
        BESTIARY_DATA.update({creature_name: {k: fix_description(v) for k, v in creature_properties.items() if k in CREATURE_DATA_KEYS} for creature_name, creature_properties in creature_collection.items()})

        # Most of the creature data is stored flat like that, but it's also important that we have a
        # record of the hierarchy between natures/species and creatures.
        creatures_just_names = { creature_key: creature_properties.get('name') for creature_key, creature_properties in creature_collection.items() }
        NATURES.setdefault(nature_key, {'name': nature_properties.get('name'), 'creatures': {}})
        NATURES[nature_key]['creatures'].update(creatures_just_names)