#!/bin/python
"""
Fetch the current type spec for KBaseGenomes
Prints the typespec to stdout
"""
import json
import os
import sys
import requests

_WS_URL = os.environ.get("WS_URL", "https://kbase.us/services/ws")
_TOK = os.environ["WS_TOK"]
_MOD_NAME = os.environ.get("MOD_NAME", "KBaseGenomes")


def main():
    """Fetch the full type spec for a module."""
    resp = requests.post(
        _WS_URL,
        headers={"Authorization": _TOK},
        data=json.dumps({
            "method": "get_module_info",
            "params": [{"mod": _MOD_NAME}]
        })
    )
    try:
        resp_json = resp.json()
    except Exception as err:
        print(err)
        print(resp.text)
        raise err
    if resp_json.get("error"):
        sys.stderr.write(resp_json["error"]["error"] + "\n")
    else:
        print(resp_json["result"][0]["spec"])


if __name__ == '__main__':
    main()
