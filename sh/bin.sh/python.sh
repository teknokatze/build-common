#!/bin/sh

# This file is part of TALER
# (C) 2019 GNUnet e.V.
#
# This is very simple POSIX sh script which
# identifies the first matching
# python3 identifier in $PATH and produces
# configure.py from configure.py.in, and then
# calls the new executable configure.py.
#
# It should be portable on Unices. Report bugs on
# the bugtracker if you discover that it isn't
# working as intended.
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

dir=$(dirname "$(readlink -- "$0")")
. $dir/../lib.sh/existence.sh
. $dir/../lib.sh/existence_python.sh

exec "$PYTHON" $@
