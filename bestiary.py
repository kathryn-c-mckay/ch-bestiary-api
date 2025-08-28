import json
import pprint
import os
from itertools import chain
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__)

NPC_LISTS = []

for path in ['datasworn/classic/classic.json', 'datasworn/delve/delve.json']:
    with open(os.path.join(BASE_DIR, path), 'r', encoding='utf-8') as f:
        NPC_LISTS.append(json.load(f).get('npcs', []))
MERGED_NPC_LISTS = {}
for npc_list in NPC_LISTS:
    for species, species_properties in npc_list.items():
        beasts = species_properties.get('contents')
        # print(species, beasts.keys())
        for beast, beast_properties in species_properties.get('contents', {}).items():
            # print(beast, beast_properties.keys())
            MERGED_NPC_LISTS.setdefault(species, {})[beast] = {k:v for k,v in beast_properties.items() if k in ['name', 'rank', 'nature', 'features', 'drives', 'tactics', 'description']}
        
        # temp_npc_list = MERGED_NPC_LISTS.get(species, {})
        # for beast, beast_properties in species_properties.get('contents', {}).items():
        #     temp_npc_list.setdefault(species, {}).update(beast_properties)
        # print(list(temp_npc_list.keys()), [list(x.keys()) for x in temp_npc_list.values()][0])
        # MERGED_NPC_LISTS.update(temp_npc_list)
    
def convert_beast_name(beast_name):
    return beast_name # TODO: fix this

# @app.route("/")
# def hello_world():
#     return BASE_DIR

@app.route("/species")
def species():
    # return {species: [beast.get('name') for beast in species.get('contents').values()] for species in MERGED_NPC_LISTS.values()}
    return {species: list(beasts.keys()) for species, beasts in MERGED_NPC_LISTS.items()}

# TODO: restore this & handle commented out stuff elsewhere
@app.route("/beast/<string:param_beast_name>")
def beast(param_beast_name):
    beast_name = convert_beast_name(param_beast_name)
    matches = chain([[record[1] for record in species.get('contents', {}).items() if record[0] == beast_name] for species in MERGED_NPC_LISTS.values() ])
    return list(matches)

# @app.route("/different-page")
# def different_page():
#     return "<p>ARE YOU NOT ENTERTAINED</p>"



app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    # print(MERGED_NPC_LISTS)
    pprint.pprint(species())
    # app.run(host='0.0.0.0')