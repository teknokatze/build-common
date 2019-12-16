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

errmsg=''

# Check if shell supports builtin 'type'.
if test -z "$errmsg"; then
    if ! (eval 'type type') >/dev/null 2>&1
    then
        errmsg='Shell does not support type builtin'
        exit 1
    fi
fi

existence()
{
    type "$1" >/dev/null 2>&1
}
