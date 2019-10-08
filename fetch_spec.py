#!/bin/python
"""
Fetch the current type spec for KBaseGenomes
Prints the typespec to stdout
"""
import json
import os
import sys
import requests

_WS_URL = "https://ci.kbase.us/services/ws"
_TOK = os.environ["WS_TOK"]
_SPEC_PATH = "./kbase_genomes_module_updated.spec"
_MOD_NAME = "KBaseGenomes"


def main():
    """Fetch the full type spec for a module."""
    resp = requests.post(
        _WS_URL,
        headers={"Authorization": _TOK},
        data=json.dumps({
            "method": "get_module_info",
            "params": [{"mod": "KBaseGenomes"}]
        })
    )
    resp_json = resp.json()
    if resp_json.get("error"):
        sys.stderr.write(resp_json["error"]["error"] + "\n")
    else:
        print(resp_json["result"][0]["spec"])


if __name__ == '__main__':
    main()
