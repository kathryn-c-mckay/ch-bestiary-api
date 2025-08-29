import os
import json
from itertools import chain
from collections import ChainMap

BASE_DIR = os.path.dirname(__file__)
BEAST_DATA_KEYS = ['name', 'rank', 'nature', 'features', 'drives', 'tactics', 'description']
BESTIARY_DATA = {}
NATURES = {}
for path in ['datasworn/classic/classic.json', 'datasworn/delve/delve.json']:
    with open(os.path.join(BASE_DIR, path), 'r', encoding='utf-8') as f:
        npc_list = json.load(f).get('npcs', [])
    for nature_key, nature_properties in npc_list.items():
        # Read in beasts from this source book. E.g.
        #  { ...
        #      'iron-wracked-beast': {
        #          'name': 'Iron-Wracked Beast',
        #          'rank': ...,
        #          'nature': 'beast',
        #       }
        #  }
        beast_collection = { orig_beast_key.replace('_', '-'): beast_properties for orig_beast_key, beast_properties in nature_properties.get('contents', {}).items() }
        BESTIARY_DATA.update({beast_name: {k: v for k, v in beast_properties.items() if k in BEAST_DATA_KEYS} for beast_name, beast_properties in beast_collection.items()})
        
        # Most of the beast data is stored flat like that, but it's also important that we have a
        # record of the hierarchy between natures/species and beasts.
        beasts_just_names = { beast_key: beast_properties.get('name') for beast_key, beast_properties in beast_collection.items() }
        NATURES.setdefault(nature_key, {'name': nature_properties.get('name'), 'beasts': {}})
        NATURES[nature_key]['beasts'].update(beasts_just_names)