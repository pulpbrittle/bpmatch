#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import fnmatch
import re
import os


def find_py(path):
    """Used to find all python files (recursively) in the directory
    
    Args:
        path (str): a path to search .py files in the module

    Example:
        >>> find_py('/home/pulpbrittle')
        ['/home/pulpbrittle/foo.py',
         '/home/pulpbrittle/bar.py']
    
    """
    pyfiles = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.py'):
            pyfiles.append(os.path.join(root, filename))
    return pyfiles


def find_bp(lst, verbose=None):
    """Used to find the defined blueprints in a module

    Args:
        lst (list): a list of .py files in the module
        verbose (bool): prints verbose information

    Example:
        >>> find_bp(['/home/pulpbrittle/foo.py',
                     '/home/pulpbrittle/bar.py'])
        ["mod = Blueprint('orders', __name__, url_prefix='/orders')",
         "mod = Blueprint('shipping', __name__, url_prefix='/shipping')"]

    """
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
        """Used to split all the parameters of the blueprint
        

        Example:
            >>> raw_bp = ["mod = Blueprint('orders', __name__)",
                          "mod = Blueprint('shipping', __name__)"]
            >>> split_bp(raw_bp)
            ['orders', 'shipping']

        """
        params = []
        p = re.compile(ur'\(\s*([^)]+?)\s*\)')
        for _ in bp:
            for match in p.findall(_):
                params.append(match.split(', ')[0])
        return params

    return split_bp()
