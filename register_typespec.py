#!/bin/python
"""
Register the genome type with the workspace server.
"""
import json
import os
import sys
import requests

_WS_URL = "https://ci.kbase.us/services/ws"
_TOK = os.environ['WS_TOK']
_SPEC_PATH = "./kbase_genomes_module.spec"


def get_spec():
    resp = requests.post(
        _WS_URL,
        headers={'Authorization': _TOK},
        data=json.dumps({
            'method': 'get_module_info',
            'params': [{
                'mod': 'KBaseGenomes'
            }]
        })
    )
    resp_json = resp.json()
    if resp_json.get('error'):
        sys.stderr.write(resp_json['error']['error'] + "\n")
    else:
        return resp_json['result'][0]['spec']


def main():
    with open(_SPEC_PATH) as fd:
        spec = fd.read()
    # Make the workspace server method call
    resp = requests.post(
        _WS_URL,
        headers={"Authorization": _TOK},
        data=json.dumps({
            "method": "register_typespec",
            "params": [{
                "spec": spec,
                "dryrun": 1,
            }],
        })
    )
    resp_json = resp.json()
    if resp_json.get('error'):
        sys.stderr.write(resp_json['error']['error'] + "\n")
    else:
        for (key, val) in resp_json['result'][0].items():
            print(val)


if __name__ == '__main__':
    main()
