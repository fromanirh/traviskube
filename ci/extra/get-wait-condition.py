#!/usr/bin/env python3

import collections
import sys


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


def _main():
    # see: https://kubevirt.io/user-guide/docs/latest/administration/intro.html#cluster-side-add-on-deployment
    cutoff = Version.from_string("v0.20.0")
    try:
        current = Version.from_string(sys.argv[1])
    except (IndexError, ValueError):
        # FIXME: that's bad practice
        sys.exit(1)

    print('Available' if current >= cutoff else 'Ready')


if __name__ == "__main__":
    _main()
