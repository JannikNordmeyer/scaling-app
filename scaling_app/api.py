import requests
import json

from scaling_app import constants


def request_lattice(objects, attributes, incidence, draw_type="freese-layout"):
    data = {
        "id": "Request",
        "context": {"type": "context",  # call function
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},

        "lattice": {"type": "function",
                    "name": "concept-lattice",
                    "args": ["context"]},
        "layout": {"type": "function",
                   "name": draw_type,
                   "args": ["lattice"]},
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post('http://127.0.0.1:8080', data=json.dumps(data, indent=4), headers=headers)

    return response.json()


def request_implications(objects, attributes, incidence, draw_type=constants.dim):
    data = {
        "id": "Request",
        "context": {"type": "context",  # call function
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},

        "lattice": {"type": "function",
                    "name": "concept-lattice",
                    "args": ["context"]},
        "layout": {"type": "function",
                   "name": draw_type,
                   "args": ["lattice"]},
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post('http://127.0.0.1:8080', data=json.dumps(data, indent=4), headers=headers)

    return response.json()