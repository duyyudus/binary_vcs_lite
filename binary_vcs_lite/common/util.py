import os
import sys
import functools
import time
import json
import re
import shutil
import copy
from pprint import pformat

if sys.version_info[0] == 3:
    from pathlib import Path, PurePath
else:
    from pathlib2 import Path, PurePath

from .config import *

_log_on = 1


class VcsLiteError(Exception):
    """Base error for version control operations."""

    def __init__(self, message=''):
        super(VcsLiteError, self).__init__()
        self._message = message
        log_error('{}'.format(message))

    def __str__(self):
        return self._message


class InvalidType(VcsLiteError):
    """Invalid type."""


def _time_measure(func):
    """Measure running time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        log_info('Running time of {}() : {} seconds'.format(func.__name__, str(time.time() - st)))
        return ret
    return wrapper


def _log_message(args):
    def fstr(s):
        if type(s) is str:
            return s
        else:
            return '\n' + pformat(s)

    _log_indent = 0
    message = ''.join([fstr(a) for a in args])
    return (''.join([' ' for i in range(_log_indent * 4)]), message)


def log_info(*args):
    if not _log_on:
        return 0
    indent_str, message = _log_message(args)
    if not message:
        print('')
        return 0
    print('{} :: {}'.format(
        LOG_PREFIX,
        indent_str + message
    ))


def log_error(*args):
    if not _log_on:
        return 0
    indent_str, message = _log_message(args)
    if not message:
        print('')
        return 0
    print('{} {} :: {}'.format(
        LOG_PREFIX,
        LOG_ERROR_PREFIX,
        indent_str + message
    ))


def switch_log_vcs(is_on):
    global _log_on
    _log_on = is_on


def match_regex_pattern(input_str, patterns):
    """
    Args:
        input_str (str):
        patterns (list of str):
    Returns:
        bool:
    """
    for p in patterns:
        if re.findall(p, input_str):
            return 1


def copy_file(source, target, overwrite=0, verbose=0):
    """Copy file and return result code.

    `source` and `target` will be converted to `str`.

    Args:
        source (str|Path):
        target (str|Path):
    Returns:
        bool:
    """

    source = str(source)
    target = str(target)

    if not Path(target).parent.exists():
        try:
            Path(target).parent.mkdir(parents=1)
        except Exception as e:
            if verbose:
                log_info('Copy mkdir error: {}'.format(target))
                log_info('----{}'.format(str(e)))
            return 0

    if overwrite and Path(target).exists():
        try:
            os.remove(target)
        except Exception as e:
            if verbose:
                log_info('Copy overwrite error: {}'.format(target))
                log_info('----{}'.format(str(e)))
            return 0

    if Path(target).exists():
        return 1
    else:
        try:
            shutil.copyfile(source, target)
        except Exception as e:
            if Path(target).exists():
                try:
                    os.remove(target)
                except Exception as e:
                    pass
            if verbose:
                log_info('Copy error: {}'.format(target))
                log_info('----{}'.format(str(e)))
            return 0
        if verbose:
            log_info('Copied: {}'.format(target))
        return 1


def batch_copy(path_pair, overwrite=0, verbose=0):
    """
    Args:
        path_pair (list of 2-tuple): List of 2-tuple of str, [(source, target),...]

    Returns:
        list of str: List of copied file paths
    """

    copied = []
    for source, target in path_pair:
        if copy_file(source, target, overwrite, verbose=verbose):
            copied.append(str(target))

    return copied


def load_json(json_path, verbose=0):
    """
    Args:
        json_path (str|Path):

    """

    json_path = Path(json_path)
    if not json_path.exists():
        if verbose:
            log_info('JSON not found: {}'.format(json_path))
        return {}

    with open(str(json_path), 'r') as f:
        if verbose:
            log_info('Loaded JSON: {}'.format(json_path))
        return json.loads(f.read())


def save_json(data, json_path, verbose=0):
    """
    Args:
        json_path (str|Path):

    """

    json_path = Path(json_path)
    if not json_path.parent.exists():
        json_path.parent.mkdir(parents=1)
    with open(str(json_path), 'w') as f:
        f.write(json.dumps(data, indent=2))
        if verbose:
            log_info('Saved JSON: {}'.format(json_path))


def check_type(obj, types, raise_exception=1):
    """Assert type of `obj`

    Args:
        obj:
        types (list): list of types/classes
    Raises:
        InvalidType:
    Returns:
        bool:
    """

    if str in types and sys.version_info[0] == 2:
        types.append(unicode)

    if isinstance(obj, tuple(types)):
        return 1
    elif raise_exception:
        msg = '"{}" ({}) must be an instance of ({})'.format(
            str(obj),
            type(obj),
            ', '.join([str(t) for t in types])
        )
        raise InvalidType(msg)
    else:
        return 0


def make_hidden(input_path):
    """Make file/folder hidden ( window only so far )
    Args:
        input_path (str|Path):
    """
    check_type(input_path, [str, Path])

    input_path = str(input_path)
    try:
        os.system('attrib +h {}'.format(input_path))
    except Exception as e:
        log_error('Cannot make hidden: {}'.format(input_path))
        log_error(str(e))
