import requests
import json

from scaling_app import constants


def request_lattice(address, objects, attributes, incidence, draw_type="freese-layout"):
    data = {
        "id": "Request",
        "context": {"type": "context",
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

    response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)

    return response.json()


def request_layout_from_lattice(address, lattice):
    data = {
        "id": "Request",

        "layout": {"type": "function",
                   "name": constants.dim,
                   "args": [lattice]},
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)

    return response.json()


def request_implications_canonical(address, objects, attributes, incidence):
    data = {
        "id": "Request",
        "context": {"type": "context",
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},

        "implications": {"type": "function",
                         "name": "canonical-base",
                         "args": ["context"]},
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)
        return response.json()
    except:
        return None


def request_implications_ganter(address, objects, attributes, incidence):
    data = {
        "id": "Request",
        "context": {"type": "context",
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},

        "implications_canon": {"type": "function",
                               "name": "canonical-base",
                               "args": ["context"]},
        "implications_ganter": {"type": "function",
                                "name": "ganter-base",
                                "args": ["implications_canon"]},
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)
        return response.json()
    except:
        return None


def request_rules(address, objects, attributes, incidence, minsupp, minconf):
    data = {
        "id": "Request",
        "context": {"type": "context",
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},
        "minsupp": {"type": "float",
                    "data": minsupp},
        "minconf": {"type": "float",
                    "data": minconf},
        "rules": {"type": "function",
                  "name": "luxenburger-base",
                  "args": ["context", "minsupp", "minconf"]},
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)
        return response.json()
    except:
        return None


def request_concepts(address, objects, attributes, incidence):
    data = {
        "id": "Request",
        "context": {"type": "context",
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},
        "concepts": {"type": "function",
                     "name": "concepts",
                     "args": ["context"]},
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)
        return response.json()
    except:
        return None


def check_connection(address):
    data = {
        "id": "Establish Connection",
        "version": {"type": "function",
                    "name": "conexp-version",
                    "args": []},
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)
        return response.json()["version"]["result"] == constants.api_version

    except:
        return False
