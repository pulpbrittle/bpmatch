#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import fnmatch
import re
import os


def find_py(path):
    """used to find all python files (recursively) in the directory"""
    pyfiles = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.py'):
            pyfiles.append(os.path.join(root, filename))
    return pyfiles


def find_bp(lst, verbose=None):
    """used to find the defined blueprints in a module"""
    bp = []
    p = re.compile('[a-zA-Z_0-9]+\s\=\sBlueprint\((.*)\)')

    for path in lst:
        with open(path, 'r') as fh:
            for number, line in enumerate(fh):
                if p.match(line):
                    line = line.replace('\'', '')
                    bp.append(line.strip())
                    if verbose:
                        print '{:03d}->{} └── {}'.format(number, line, path)

    def split_bp():
        """used to split all the parameters of the blueprint"""
        params = []
        p = re.compile(ur'\(\s*([^)]+?)\s*\)')
        for _ in bp:
            for match in p.findall(_):
                params.append(match.split(', ')[0])
        return params
    return split_bp()
