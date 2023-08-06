
import json

version_json = '''
{"date": "2020-08-13T17:55:34.197044", "dirty": false, "error": null, "full-revisionid": "5aa507b1037f5c78a02a4cc3e962a379905d5249", "version": "0.19.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

