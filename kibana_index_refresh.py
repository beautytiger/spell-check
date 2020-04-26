#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ref: https://github.com/elastic/kibana/issues/6498
# ref: https://github.com/idaholab/Malcolm/blob/master/kibana/scripts/kibana_index_refresh.py

from __future__ import print_function

import argparse
import json
import requests
import os
import sys

auth = ("elastic", "giJIyZsmWH48TFzxNAPs")

GET_STATUS_API = "api/status"
GET_INDEX_PATTERN_INFO_URI = "api/saved_objects/index-pattern"
GET_FIELDS_URI = "api/index_patterns/_fields_for_wildcard"
PUT_INDEX_PATTERN_URI = "api/saved_objects/index-pattern"
GET_INDEX_PATTERNS = (
    "api/saved_objects/_find?fields=title&per_page=10000&type=index-pattern"
)

###################################################################################################
debug = False
PY3 = sys.version_info.major >= 3
scriptName = os.path.basename(__file__)
scriptPath = os.path.dirname(os.path.realpath(__file__))
origPath = os.getcwd()

###################################################################################################
if not PY3:
    if hasattr(__builtins__, "raw_input"):
        input = raw_input

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


###################################################################################################
# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


###################################################################################################
# convenient boolean argument parsing
def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


###################################################################################################
# main
def main():
    global debug

    parser = argparse.ArgumentParser(
        description=scriptName,
        add_help=False,
        usage="{} <arguments>".format(scriptName),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="debug",
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        help="Verbose output",
    )
    parser.add_argument(
        "-i",
        "--index",
        dest="index",
        metavar="<str>",
        type=str,
        default="sessions2-*",
        help="Index Pattern Name",
    )
    parser.add_argument(
        "-k",
        "--kibana",
        dest="url",
        metavar="<protocol://host:port>",
        type=str,
        default="http://10.20.123.19:31637",
        help="Kibana URL",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        dest="dryrun",
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        help="Dry run (no PUT)",
    )
    try:
        parser.error = parser.exit
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit(2)

    debug = args.debug
    if debug:
        eprint(os.path.join(scriptPath, scriptName))
        eprint("Arguments: {}".format(sys.argv[1:]))
        eprint("Arguments: {}".format(args))
    else:
        sys.tracebacklimit = 0

    # get version number so kibana doesn't think we're doing a XSRF when we do the PUT
    statusInfoResponse = requests.get(
        "{}/{}".format(args.url, GET_STATUS_API), auth=auth
    )
    statusInfoResponse.raise_for_status()
    print("response status code: ", statusInfoResponse.status_code)
    statusInfo = statusInfoResponse.json()
    kibanaVersion = statusInfo["version"]["number"]
    if debug:
        eprint("Kibana version is {}".format(kibanaVersion))

    # get all index patterns
    getIndexpatternsResponse = requests.get(
        "{}/{}".format(args.url, GET_INDEX_PATTERNS), auth=auth
    )
    getIndexpatternsResponse.raise_for_status()
    getIndexInfo = getIndexpatternsResponse.json()
    indices = getIndexInfo["saved_objects"]
    if debug:
        eprint("all the indices {}".format(indices))
    for index in indices:
        index_name = index["attributes"]["title"]
        index_id = index["id"]
        try:
            handle_index_pattern(index_id, index_name, args, kibanaVersion)
        except Exception as e:
            # will panic if target index not exist in system: 404 Client Error
            eprint("##############################>", e)
            eprint("------------------------------>", index_name, index_id)
            continue

    # if we got this far, it probably worked!
    if args.dryrun:
        print("success (dry run only, no write performed)")
    else:
        print("success")


def handle_index_pattern(index_id, index_name, args, kibanaVersion):

    # get the ID of the index name (probably will be the same as the name)
    # getIndexInfoResponse = requests.get(
    #   "{}/{}/{}".format(args.url, GET_INDEX_PATTERN_INFO_URI, index_name), auth=auth
    # )
    # getIndexInfoResponse.raise_for_status()
    # getIndexInfo = getIndexInfoResponse.json()
    indexId = index_id
    if debug:
        eprint("Index ID for {} is {}".format(index_name, indexId))

    # get the fields list
    getFieldsResponse = requests.get(
        "{}/{}".format(args.url, GET_FIELDS_URI),
        params={
            "pattern": index_name,
            "meta_fields": ["_source", "_id", "_type", "_index", "_score"],
        },
        auth=auth,
    )
    getFieldsResponse.raise_for_status()
    getFieldsList = getFieldsResponse.json()["fields"]
    if debug:
        eprint("{} would have {} fields".format(index_name, len(getFieldsList)))

    # set the index pattern with our complete list of fields
    if not args.dryrun:
        putIndexInfo = {}
        putIndexInfo["attributes"] = {}
        putIndexInfo["attributes"]["title"] = index_name
        putIndexInfo["attributes"]["fields"] = json.dumps(getFieldsList)

        putResponse = requests.put(
            "{}/{}/{}".format(args.url, PUT_INDEX_PATTERN_URI, indexId),
            headers={
                "Content-Type": "application/json",
                "kbn-xsrf": "true",
                "kbn-version": kibanaVersion,
            },
            data=json.dumps(putIndexInfo),
            auth=auth,
        )
        putResponse.raise_for_status()


if __name__ == "__main__":
    main()
