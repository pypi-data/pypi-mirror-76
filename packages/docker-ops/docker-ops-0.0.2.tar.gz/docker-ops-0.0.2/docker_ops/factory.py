#!/usr/bin/env python

import argparse
import os

def obtain_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scan', default=False, action='store_true',
            help='Scan the directory for folders with a Dockerfile, and build them')
    parser.add_argument('-d', '--directory', default=os.getcwd(), type=str,
            help='Which directory should docker_ops scan?')
    return parser.parse_args()

def main() -> None:
    options = obtain_options()
    if options.scan:
        from docker_ops import scan
        scan.scan_and_build(options.directory)

def run_from_cli() -> None:
    import sys, os
    sys.path.append(os.getcwd())
    main()

if __name__ == '__main__':
    main()
