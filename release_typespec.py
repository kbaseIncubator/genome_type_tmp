#!/bin/python
"""
Relase the KBaseGenomes typespec using the release_module method from the workspace server api
"""
import json
import os
import requests

_WS_URL = "https://ci.kbase.us/services/ws"
_TOK = os.environ["WS_TOK"]
_MOD_NAME = "KBaseGenomes"


def main():
    """Make the method call to relase KBaseGenomes."""
    resp = requests.post(
        _WS_URL,
        headers={"Authorization": _TOK},
        data=json.dumps({
            "method": "release_module",
            "params": [_MOD_NAME],
        })
    )
    resp_json = resp.json()
    print(json.dumps(resp_json, indent=2))


if __name__ == '__main__':
    main()
