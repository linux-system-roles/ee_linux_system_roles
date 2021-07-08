#!/usr/bin/env python
"""Update requirements.yml with latest collection versions."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import yaml


# NOTE: If we were to implement this with the REST API, we would have to
# page through the versions, exclude the ones that don't match StrictVersion
# X.Y.Z, sort with LooseVersion to get the highest . . . imo, better to
# let ansible-galaxy do all of that work for us
def get_latest_version(collection):
    """Get the latest version of the given collection"""
    coll_dir = tempfile.mkdtemp()
    cmd = [
        "ansible-galaxy", "collection", "install", "-n", "-vv", "--force",
        "-p", coll_dir, collection
    ]
    try:
        out = subprocess.run(cmd, stdout=subprocess.PIPE, encoding="utf-8")
        pat = f"Installing '{collection}:([^']+)' to"
        item = re.search(pat, out.stdout)
        return item.group(1)
    finally:
        shutil.rmtree(coll_dir)


def main():
    """Run it."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--requirements-yml",
        type=str,
        default=os.environ.get("REQUIREMENTS_YML", "requirements.yml"),
        help="Path/filename for requirements.yml",
    )
    parser.add_argument(
        "--coll-vers-to-print",
        action="append",
        help=(
            "Print the versions of the given collections if they are updated "
            "The versions are printed in the order given.  If there is no "
            "version update, the output will be the literal string 'NONE'."
        ),
    )
    args = parser.parse_args()
    if not args.coll_vers_to_print:
        args.coll_vers_to_print = ["fedora.linux_system_roles"]
    hsh = yaml.safe_load(open(args.requirements_yml))
    collhash = {}
    changed = False
    for coll in hsh["collections"]:
        latest_ver = get_latest_version(coll["name"])
        cur_ver = coll.get("version")
        if latest_ver != cur_ver:
            changed = True
            coll["version"] = latest_ver
            collhash[coll["name"]] = latest_ver
        else:
            collhash[coll["name"]] = "NONE"
    if changed:
        yaml.safe_dump(
            hsh, open(args.requirements_yml, "w"), default_flow_style=False
        )
    for collname in args.coll_vers_to_print:
        print(collhash[collname])


if __name__ == "__main__":
    sys.exit(main())
