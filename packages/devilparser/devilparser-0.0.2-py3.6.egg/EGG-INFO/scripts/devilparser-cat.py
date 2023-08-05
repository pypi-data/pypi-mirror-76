#!/usr/local/opt/python3/bin/python3.6
import sys
import os
from devilparser import rcfile


def main():
    yaml_file = sys.argv[1]
    print("Parsing %s" % yaml_file)
    info = rcfile.parse(os.path.join(yaml_file)).contents()
    print(info)
    return 0

if __name__ == "__main__":
    sys.exit(main())
