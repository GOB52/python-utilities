#! /usr/bin/env python3
#
# Raise Version by semantics versioning for Arduino library
#
import os
import sys
import argparse
import re
import json

LIBRARY_PROPERTY = './library.properties'
LIBRARY_JSON = './library.json'
REGEX_FOR_PROPERTY = r'^\s*version\s*=\s*(\d*.\d*.\d*)'

def get_versions(verbose = False):
    versions = []

    if os.path.exists(LIBRARY_PROPERTY):
        if verbose:
            print('Exists ' + LIBRARY_PROPERTY)
        with open(LIBRARY_PROPERTY, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            for line in lines:
                m = re.match(REGEX_FOR_PROPERTY, line)
                if m:
                    versions.append(m.groups()[0])

    if os.path.exists(LIBRARY_JSON):
        if verbose:
            print('Exists ' + LIBRARY_JSON)
        with open(LIBRARY_JSON, 'r') as f:
            j = json.load(f)
            if 'version' in j.keys():
                versions.append(j['version'])

    return versions

def raise_property_version(major, minor, patch):
    nlines = []

    with open(LIBRARY_PROPERTY, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            m = re.match(REGEX_FOR_PROPERTY, line)
            if m:
                nlines.append('version={}.{}.{}\n'.format(major, minor, patch))
            else:
                nlines.append(line)
            
        f.truncate(0)
        f.seek(0)
        f.writelines(nlines)


def raise_json_version(major, minor, patch):
    j = dict()
    with open(LIBRARY_JSON, 'r+') as f:
        j = json.load(f)
        if 'version' in j.keys():
            j['version'] = '{}.{}.{}'.format(major, minor, patch)

        f.truncate(0)
        f.seek(0)
        json.dump(j, f, ensure_ascii=False, indent=2)


def output_header(path, prefix, major, minor, patch):

    with open(path, 'w') as f:
        print('#ifndef {}_VERSION_HPP\n#define {}_VERSION_HPP\n'.format(prefix, prefix), file=f)
        print('#define {}_VERSION_MAJOR {}'.format(prefix, major), file=f)
        print('#define {}_VERSION_MINOR {}'.format(prefix, minor), file=f)
        print('#define {}_VERSION_PATCH {}\n'.format(prefix, patch), file=f)
        print('#define {}_VERSION_STRINGIFY_AGAIN(x) #x'.format(prefix), file=f)
        print('#define {}_VERSION_STRINGIFY(x) {}_VERSION_STRINGIFY_AGAIN(x)\n'.format(prefix, prefix), file=f)
        print('#define {}_VERSION_VALUE (({}_VERSION_MAJOR << 16) | ({}_VERSION_MINOR << 8) | ({}_VERSION_PATCH))'.format(prefix, prefix, prefix, prefix), file=f)
        print('#define {}_VERSION_STRING {}_VERSION_STRINGIFY({}_VERSION_MAJOR.{}_VERSION_MINOR.{}_VERSION_PATCH)\n'.format(prefix, prefix, prefix, prefix, prefix), file=f)
        print('#endif', file=f)


def main():
    parser = argparse.ArgumentParser(description='Raise Version by semantics versioning.')

    parser.add_argument('--execute', '-e', action='store_true', help="Do raising. dry-run if not set")
    parser.add_argument('--raising', '-r', default='PATCH', choices=['MAJOR','MINOR', 'PATCH'], help='Increment target (PATCH as default)')
    parser.add_argument('--source', '-s', type=str, help='Output source file path')
    parser.add_argument('--prefix', '-p', type=str, help='Definition prefix for source (require if --source)')
    parser.add_argument('--info', '-i', action='store_true', help='Show version from property and json if exists')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    if args.source:
        if args.prefix is None:
            parser.error('--prefix must need if --source exists')

    versions = get_versions(args.verbose)

    if len(versions) == 0:
        print('Unable to read version from propery or json')
        return -1

    if args.info or args.verbose:
        print(versions)

    if len(versions) > 1:
        versions = list(set(versions)) # unique
        if len(versions) != 1:
            print('Each version is different. Is it true?')
            return 1

    if args.info:
        return 0

    version = versions[0].split('.')
    major, minor, patch = [int(v) for v in version]
    omajor = major = major or 0
    ominor = minor = minor or 0
    opatch = patch = patch or 0

    if args.verbose:
        print('Raise {} from {}.{},{}'.format(args.raising, major, minor, patch))

    if args.raising == 'PATCH':
        patch += 1
    elif args.raising == 'MINOR':
        minor += 1
        patch = 0
    elif args.raising == 'MAJOR':
        major += 1
        minor = 0
        patch = 0
       
    # Dry-run
    if not args.execute:
        print('Dry-run : Raise from {}.{}.{} to {}.{}.{}'.format(omajor, ominor, opatch, major, minor, patch))
        print('If you want to do raising, set --execute or -e')
        return 0

    if args.verbose:
        print('Raise version to {}.{},{}'.format(major, minor, patch))

    if os.path.exists(LIBRARY_PROPERTY):
        raise_property_version(major, minor, patch)
    if os.path.exists(LIBRARY_JSON):
        raise_json_version(major, minor, patch)
    if args.source and args.prefix:
        output_header(args.source, args.prefix, major, minor, patch)

    print('Raised version to {}.{}.{} successfully'.format(major, minor, patch))

    return 0


if __name__ == '__main__':
    sys.exit(main())

