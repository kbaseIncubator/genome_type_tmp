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
_SPEC_URL = "https://raw.githubusercontent.com/kbaseIncubator/genome_type_tmp/c38b449c115060f28fa8422d6f410bb1657bd1a4/genome.spec"  # noqa


def main():
    spec = requests.get(_SPEC_URL).text
    # Wrap the spec in the module name
    spec = "module KBaseGenomes {\n" + spec + "\n}\n"
    # Make the workspace server method call
    resp = requests.post(
        _WS_URL,
        headers={"Authorization": _TOK},
        data=json.dumps({
            "method": "register_typespec",
            "params": [{
                "spec": spec,
                "dryrun": 1,
                "dependencies": {
                    # TODO this does not work
                    "KBaseGenomes": "Feature-7.0"
                }
            }],
        })
    )
    resp_json = resp.json()
    if resp_json['error']:
        sys.stderr.write(resp_json['error']['error'] + "\n")


if __name__ == '__main__':
    main()
