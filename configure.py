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

"""
This application aims to replicate a small GNU Coding Standards
configure script, taylored at projects in GNU Taler. We hope it
can be of use outside of GNU Taler, hence it is dedicated to the
public domain ('0BSD').
It takes a couple of arguments on the commandline equivalent to
configure by autotools, in addition some environment variables
xan take precedence over the switches. In the absence of switches,
/usr/local is assumed as the PREFIX.
When  all data from tests are gathered, it generates a config.mk
Makefile fragement, which is the processed by a Makefile (usually) in
GNU Make format.
"""


def existence(name):
    return find_executable(name) is not None


def tool_version(name):
    return subprocess.getstatusoutput(name)[1]


def tool_emscripten():
    if existence('emcc'):
        emscripten_version = tool_version('emcc --version')
        return f"emscripten version {emscripten_version} found"
    else:
        return f"emscripten compiler not found"


def tool_pybabel():
    # No suffix. Would probably be cheaper to do this in
    # the dict as well.
    if existence('pybable'):
        return 'pybable'
    else:
        # Has suffix, try suffix. We know the names in advance,
        # so use a dictionary and iterate over it. Use enough names
        # to safe updating this for another couple of years.
        #
        # Food for thought: If we only accept python 3.7 or higher,
        # is checking pybabel + pybabel-3.[0-9]* too much and could
        # be broken down to pybabel + pybabel-3.7 and later names?
        version_dict = {
            '3.0': 'pybabel-3.0',
            '3.1': 'pybabel-3.1',
            '3.2': 'pybabel-3.2',
            '3.3': 'pybabel-3.3',
            '3.4': 'pybabel-3.4',
            '3.5': 'pybabel-3.5',
            '3.6': 'pybabel-3.6',
            '3.7': 'pybabel-3.7',
            '3.8': 'pybabel-3.8',
            '3.9': 'pybabel-3.9',
            '4.0': 'pybabel-4.0',
        }
        for value in version_dict.values():
            if existence(value):
                return value


def tool_browser():
    # TODO: read xdg-open value first.
    browser_dict = {
        'ice': 'icecat',
        'ff': 'firefox',
        'chg': 'chrome',
        'ch': 'chromium',
        'o': 'opera'
    }
    if 'BROWSER' in os.environ:
        return os.environ.get('BROWSER')
    else:
        for value in browser_dict.values():
            if existence(value):
                return value


def tool_node():
    if existence('node') is None:
        sys.exit(
            'Error: node executable not found.\nIf you are using Ubuntu Linux or Debian Linux, try installing the\nnode-legacy package or symlink node to nodejs.'
        )
    else:
        if subprocess.getstatusoutput(
            "node -p 'process.exit(!(/v([0-9]+)/.exec(process.version)[1] >= 4))'"
        )[1] is not '':
            sys.exit('Your node version is too old, use Node 4.x or newer')
        else:
            node_version = tool_version("node --version")
            return f"Using Node version {node_version}"


def tool_yarn():
    if existence('yarn'):
        p1 = subprocess.run(['yarn', 'help'],
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE)
        if 'No such file or directory' in p1.stdout.decode('utf-8'):
            if existence('cmdtest'):
                print(
                    'WARNING: cmdtest is installed, this can lead\nto know issues with yarn.'
                )
            sys.exit(
                'ERROR: You seem to have the wrong kind of "yarn" installed, please remove the\nconflicting binary before continuing!'
            )
        return 'yarn'
    elif existence('yarnpkg'):
        return 'yarnpkg'
    else:
        sys.exit(
            'ERROR: yarn missing. See https://yarnpkg.com/en/docs/install\n'
        )


def tool_posix():
    messages = []

    tool_find = existence('find')
    if tool_find is None:
        messages.append('prerequisite find(1) not found.')

    tool_xargs = existence('xargs')
    if tool_xargs is None:
        messages.append('prerequisite xargs(1) not found.')

    tool_msgmerge = existence('msgmerge')
    if tool_msgmerge is None:
        messages.append('prerequisite msgmerge(1) not found.')

    return messages


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--prefix',
        type=str,
        default='/usr/local',
        help='Directory prefix for installation'
    )
    parser.add_argument(
        '-yarn', '--with-yarn', type=str, help='name of yarn executable'
    )
    parser.add_argument(
        '-browser',
        '--with-browser',
        type=str,
        help='name of your webbrowser executable'
    )
    parser.add_argument(
        '-pybabel',
        '--with-pybabel',
        type=str,
        help='name of your pybabel executable'
    )
    args = parser.parse_args()
    if 'DEBUG' in os.environ:
        logger.debug('%s', args)

    # get PREFIX
    if 'PREFIX' in os.environ:
        p_myprefix = os.environ.get('PREFIX')
        if p_myprefix is not None and os.path.isdir(p_myprefix) is True:
            myprefix = p_myprefix
    elif args.prefix is not '/usr/local':
        myprefix = args.prefix
    else:
        myprefix = parser.get_default('prefix')

    # get yarn executable
    if args.with_yarn is not None:
        yarnexe = args.with_yarn
    else:
        yarnexe = str(tool_yarn())

    mybrowser = tool_browser()
    mypybabel = tool_pybabel()
    f = open('config.mk', 'w+')
    f.writelines([
        '# This mk fragment is autogenerated by configure.py\n',
        f'prefix={myprefix}\n', f'yarnexe={yarnexe}\n',
        f'RUN_BROWSER={mybrowser}\n', f'pybabel={mypybabel}\n'
    ])
    f.close()
    print(tool_node())
    print(tool_emscripten())
    posixlist = tool_posix()
    for msg in posixlist:
        print(posixlist[msg])


if __name__ == "__main__":
    main()
