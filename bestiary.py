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
# TODO: add deep merge?
for npc_list in NPC_LISTS:
    for species, species_properties in npc_list.items():
        for beast, beast_properties in species_properties.get('contents', {}).items():
            MERGED_NPC_LISTS.setdefault(species_properties.get('name'), {})[beast_properties.get('name')] = {k:v for k,v in beast_properties.items() if k in ['rank', 'nature', 'features', 'drives', 'tactics', 'description']}

def convert_beast_name(beast_name):
    return beast_name # TODO: fix this

@app.route("/species")
def species():
    return {species: list(beasts.keys()) for species, beasts in MERGED_NPC_LISTS.items()}

# TODO: restore this & handle commented out stuff elsewhere
@app.route("/beast/<string:param_beast_name>")
def beast(param_beast_name):
    beast_name = convert_beast_name(param_beast_name)
    # matches = chain([[record[1] for record in species.get('contents', {}).items() if record[0] == beast_name] for species in MERGED_NPC_LISTS.values() ])
    # return list(matches)
    return []

@app.route("/different-page")
def different_page():
    return "<p>ARE YOU NOT ENTERTAINED</p>"

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    app.run(host='0.0.0.0')