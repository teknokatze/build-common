# This file is part of TALER
# (C) 2019 GNUnet e.V.
#
# Authors:
# Author: ng0 <ng0@taler.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE
# LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
# SPDX-License-Identifier: 0BSD

import argparse
import os
import sys
import logging
from distutils.spawn import find_executable
import subprocess
from subprocess import Popen

# This script so far generates config.mk.
# The only value it produces is prefix,
# which is either taken as the first argument
# to this script, or as --prefix=, or read
# from the environment variable PREFIX.
#
# TODO: Also respect DESTDIR ($PREFIX/$DESTDIR/rest).


def existence(name):
    return find_executable(name) is not None


def tool_version(name):
    return subprocess.getstatusoutput(name)[1]


def tool_emscripten():
    if _existence('emcc') is None:
        return f"emscripten compiler not found"
    else:
        emscripten_version = _tool_version('emcc --version')
        return f"emscripten version {emscripten_version} found"


# TODO: Extract python binary version suffix from
# sys.executable ?
def tool_pybabel():
    if _existence('pybable'):
        return 'pybable'
    # pybable is not pybable:
    # construct dictionary of possible binary names
    # try for each key if _existence(value) checks out
    # to be true.
    # if true, return the matching name


# Far from ideal list.
def tool_browser():
    if 'BROWSER' in os.environ:
        return os.environ.get('BROWSER')
    elif _existence('firefox'):
        return 'firefox'
    elif _existence('chrome'):
        return 'chrome'
    elif _existence('chromium'):
        return 'chromium'
    else:
        pass


def tool_node():
    if _existence('node') is None:
        sys.exit(
            'Error: node executable not found.\nIf you are using Ubuntu Linux or Debian Linux, try installing the\nnode-legacy package or symlink node to nodejs.'
        )
    else:
        if subprocess.getstatusoutput(
            "node -p 'process.exit(!(/v([0-9]+)/.exec(process.version)[1] >= 4))'"
        )[1] is not '':
            sys.exit('Your node version is too old, use Node 4.x or newer')
        else:
            node_version = _tool_version("node --version")
            return f"Using Node version {node_version}"


def tool_yarn():
    if _existence('yarn'):
        p1 = subprocess.run(['yarn', 'help'],
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE)
        'No such file or directory'

        if output is not b'':
            if _existence('cmdtest'):
                print(
                    'WARNING: cmdtest is installed, this can lead\nto know issues with yarn.'
                )
            sys.exit(
                'ERROR: wrong yarn binary installed, please remove the\nconflicting binary before continuing.'
            )
        return 'yarn'
    elif _existence('yarnpkg'):
        return 'yarnpkg'
    else:
        sys.exit(
            'ERROR: yarn missing. See https://yarnpkg.com/en/docs/install\n'
        )


def tool_posix():
    messages = []

    tool_find = _existence('find')
    if tool_find is None:
        messages.append('prerequisite find(1) not found.')

    tool_xargs = _existence('xargs')
    if tool_xargs is None:
        messages.append('prerequisite xargs(1) not found.')

    tool_msgmerge = _existence('msgmerge')
    if tool_msgmerge is None:
        messages.append('prerequisite msgmerge(1) not found.')

    return messages


def read_prefix():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    if 'DEBUG' in os.environ:
        logger.debug('PREFIX from argv')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--prefix',
        type=str,
        default='/usr/local',
        help='Directory prefix for installation'
    )
    parser.add_argument(
        '-y', '--yarn', type=str, help='name of yarn executable'
    )
    if 'DEBUG' in os.environ:
        logger.debug('parser.parse_args step')
    args = parser.parse_args()
    if 'DEBUG' in os.environ:
        logger.debug('%s', args)
    if 'PREFIX' in os.environ:
        if 'DEBUG' in os.environ:
            logger.debug('PREFIX from environment')
        p_myprefix = os.environ.get('PREFIX')
        if p_myprefix is not None and os.path.isdir(p_myprefix) is True:
            if 'DEBUG' in os.environ:
                logger.debug('PREFIX from environment: %s', p_myprefix)
            myprefix = p_myprefix
    elif args.prefix is not '/usr/local':
        if 'DEBUG' in os.environ:
            logger.debug('PREFIX from args.prefix')
        myprefix = args.prefix
    else:
        if 'DEBUG' in os.environ:
            logger.debug('PREFIX from args.prefix default value')
        myprefix = parser.get_default('prefix')
    if args.yarn is not None:
        yarnexe = args.yarn
    else:
        yarnexe = str(_tool_yarn())
    if 'DEBUG' in os.environ:
        logger.debug('%s', repr(myprefix))
    return [myprefix, yarnexe]


def main():
    mylist = _read_prefix()
    myprefix = mylist[0]
    yarnexe = mylist[1]
    mybrowser = _tool_browser()
    f = open('config.mk', 'w+')
    f.writelines([
        '# this file is autogenerated by ./configure\n', f'prefix={myprefix}\n',
        f'yarnexe={yarnexe}\n', f'RUN_BROWSER={mybrowser}\n'
    ])
    f.close()
    print(_tool_node())
    posixlist = _tool_posix()
    for msg in posixlist:
        print(posixlist[msg])


if __name__ == "__main__":
    main()
