import requests
import json


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


def request_implications(address, objects, attributes, incidence):
    data = {
        "id": "Request",
        "context": {"type": "context",  # call function
                    "data":
                        {"objects": objects,
                         "attributes": attributes,
                         "incidence": incidence}},

        "implications": {"type": "function",
                         "name": "canonical-base",
                         "args": ["context"]},
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)

    return response.json()


def request_rules(address, objects, attributes, incidence, minsupp, minconf):
    data = {
        "id": "Request",
        "context": {"type": "context",  # call function
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

    response = requests.post(address, data=json.dumps(data, indent=4), headers=headers)

    return response.json()
