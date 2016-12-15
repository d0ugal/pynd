import argparse
import sys

from pynd import search

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    search(args.files)

if __name__ == '__main__':
    sys.exit(main())
