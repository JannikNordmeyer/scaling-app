import requests
import json


def post(objects, attributes, incidence):
    data = {
        "id": "my request",
        "context": {"type": "context",  # call function
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},

        "lattice": {"type": "function",
                    "name": "concept-lattice",
                    "args": ["context"]},
        "layout": {"type": "function",
                   "name": "dim-draw-layout",  # ----> hier layout parameter
                   "args": ["lattice"]},
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post('http://127.0.0.1:8080', data=json.dumps(data, indent=4), headers=headers)

    return response.json()
