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


def _existence(name):
    return find_executable(name) is not None


def _tool_version(name):
    return subprocess.getstatusoutput(name)[1]


def _tool_node():
    if _existence('node') is None:
        sys.exit('Error: node executable not found.\nIf you are using Linux, Ubuntu or Debian, try installing the\nnode-legacy package or symlink node to nodejs.')
    else:
        if subprocess.getstatusoutput("node -p 'process.exit(!(/v([0-9]+)/.exec(process.version)[1] >= 4))'")[1] is not '':
            # and exit(1) here?
            sys.exit('Your node version is too old, use Node 4.x or newer')
        else:
            node_version = _tool_version("node --version")
            return f"Using Node version {node_version}"


def _tool_yarn():
    if _existence('yarn'):
        p1 = Popen(['yarn', 'help'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p2 = Popen(['grep', 'No such file or directory'], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits
        output = p2.communicate()[0]
        if output is b'':
            if _existence('cmdtest'):
                print('WARNING: cmdtest is installed, this can lead\nto know issues with yarn.')
            sys.exit('ERROR: wrong yarn binary installed, please remove the\nconflicting binary before continuing.')
        return 'yarn'
    elif _existence('yarnpkg'):
        return 'yarnpkg'
    else:
        sys.exit('ERROR: yarn missing. See https://yarnpkg.com/en/docs/install\n')


def _tool_posix():
    tool_find = _existence('find')
    if tool_find is None:
        msg_find = 'prerequiste find(1) not found.'
    else:
        msg_find = ''

    tool_xargs = _existence('xargs')
    if tool_xargs is None:
        msg_xargs = 'prerequiste xargs(1) not found.'
    else:
        msg_xargs = ''

    tool_msgmerge = _existence('msgmerge')
    if tool_msgmerge is None:
        msg_msgmerge = 'prerequiste msgmerge(1) not found.'
    else:
        msg_msgmerge = ''

    return [msg_find, msg_xargs, msg_msgmerge]


def _read_prefix():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)


    if 'DEBUG' in os.environ:
        logger.debug('PREFIX from argv')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--prefix',
                        type=str,
                        default='/usr/local',
                        help='Directory prefix for installation')
    parser.add_argument('-y',
                        '--yarn',
                        type=str,
                        help='name of yarn executable')
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
    # We should probably not check if the path exists
    # because make will throw an error anyway or create
    # it.
    # if os.path.isdir(myprefix) is True:
    return [myprefix, yarnexe];

def main():
    mylist = _read_prefix()
    myprefix = mylist[0]
    yarnexe = mylist[1]
    f = open('config.mk', 'w+')
    f.writelines(['# this file is autogenerated by ./configure\n',
                  f'prefix={myprefix}\n',
                  f'yarnexe={yarnexe}\n'])
    f.close()
    print(_tool_node())
    posixlist = _tool_posix()
    for x in range(len(posixlist)):
        if x is not '':
            print(posixlist[x] + "\n")


main()
