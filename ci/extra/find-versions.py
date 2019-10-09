#!/usr/bin/env python3

import collections
import sys
import json


_version = collections.namedtuple('_version', ['major', 'minor', 'micro'])


class Version(_version):

    @classmethod
    def from_string(cls, text):
        text = text.lstrip("v")
        text = text.split("-")[0]  # TODO: handle '-extra'?
        major, minor, micro = text.split('.')
        return cls(int(major), int(minor), int(micro))

    def __str__(self):
        return "v%d.%d.%d" % (self.major, self.minor, self.micro)


def versions(data):
    tags = [ item.get('tag_name', '') for item in data ]
    versions = [ Version.from_string(tag) for tag in tags if tag]
    buckets = {}
    for ver in versions:
        key = (ver.major, ver.minor)
        if key not in buckets:
            buckets[key] = ver
        else:
            cur = buckets[key]
            buckets[key] = ver if ver > cur else cur
    return list(reversed(sorted(buckets.values())))


def _find_ver_idx(vers, target):
    for idx, ver in enumerate(vers):
        if ver == target:
            return idx
    return None


def _has_arg():
    return (
        len(sys.argv) > 1 and
        sys.argv[1] != ""  # shell invocation artifact
    )


def _main():
    builtin = Version.from_string(sys.argv[1]) if _has_arg() else None
    vers = versions(json.load(sys.stdin))
    if not vers:
        return

    secondlast = vers[1] if len(vers) >= 1 else vers[0]
    out = {
            'last': vers[0],
            'secondlast': secondlast,
    }

    if builtin is not None:
        out['builtin'] = builtin
        # set defaults
        for key in ('previous', 'following',):
            out[key] = builtin

        # TODO: this does extract string match, may lead to surprising results
        idx = _find_ver_idx(vers, builtin)
        if idx is not None and idx < len(vers):
            out['previous'] = vers[idx+1]
        if idx is not None and idx > 1:
            out['following'] = vers[idx-1]

    print("\n".join("%s=%s" % (k, v) for k, v in out.items()))


if __name__ == "__main__":
    _main()
