#!/usr/bin/env python3

import urllib.request

DIST_URL = "https://dist.ipfs.tech"


def get_versions():
    versions_url = "{}/kubo/versions".format(DIST_URL)

    print("Getting versions from {}".format(versions_url))
    with urllib.request.urlopen(versions_url) as response:
        content = response.read().decode(
            response.headers.get_content_charset()
        )

        return content.splitlines()


def get_dist(version):
    dist_url = "{}/kubo/{}/dist.json".format(DIST_URL, version)

    print("Fetching dist from {}".format(dist_url))
    with urllib.request.urlopen(dist_url) as response:
        return response.read().decode('utf-8')


def write_version(dist, version):
    version_path = "vars/versions/{}.json".format(version)

    print("Writing dist to {}".format(version_path))
    with open(version_path, "w", encoding='utf-8') as version_file:
        version_file.write(dist)


for version in get_versions():
    dist = get_dist(version)
    write_version(dist, version)
