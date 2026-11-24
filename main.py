"""Entry program for the make.fun news-image-20261124 bounty.

What it does: copy the finished picture that ships with this repo
(entry.png, drawn at build time by draw.py) into the folder the grader
expects, /output/entry.png. The copy is byte-for-byte identical, so
running it twice writes the same bytes.

It honours MAKEFUN_OUTPUT_DIR when set (handy for local runs) and falls
back to /output otherwise. No network, no randomness, no third-party
code — only the Python standard library.
"""

import hashlib
import os
import shutil
import sys

PICTURE = "entry.png"
DEFAULT_OUT = "/output"


def repo_dir():
    return os.path.dirname(os.path.abspath(__file__))


def out_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUT


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(repo_dir(), PICTURE)
    if not os.path.isfile(src):
        print("missing %s next to main.py" % PICTURE, file=sys.stderr)
        return 1
    folder = out_dir()
    os.makedirs(folder, exist_ok=True)
    dst = os.path.join(folder, PICTURE)
    shutil.copyfile(src, dst)
    before, after = sha256_of(src), sha256_of(dst)
    print("copied %s -> %s" % (src, dst))
    print("sha256 in : %s" % before)
    print("sha256 out: %s" % after)
    if before != after:
        print("ERROR: output hash differs from the bundled picture",
              file=sys.stderr)
        return 2
    print("OK: output is identical to the bundled picture")
    return 0


if __name__ == "__main__":
    sys.exit(main())
