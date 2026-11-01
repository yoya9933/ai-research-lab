"""Original BSD-licensed Pygments PR #3190 regression functions.
Test function bodies are verbatim from tests/test_regexopt.py at
64226095eb736dbf23e16786f04c82f3a3a86b92 (Git blob
f2d566541c37ac8b7ab35b239bdea4aeea565b56).
Only imports are adapted to the standalone pinned regexopt.py.
See LICENSE in this case directory.
"""

import re
from regexopt import regex_opt


def test_duplicates():
    # duplicate words must not produce a redundant character class like [ss]
    opt = regex_opt(('as', 'abstract', 'and', 'as', 'break'))
    print(opt)
    assert '[ss]' not in opt
    rex = re.compile(opt)
    assert rex.match('as')
    assert rex.match('abstract')
    assert rex.match('and')
    assert rex.match('break')
    assert not rex.match('x')
    assert rex.groups == 1


def test_duplicate_single_chars():
    # duplicate one-character words must be collapsed in the character class
    opt = regex_opt(('a', 'a', 'b'))
    print(opt)
    assert opt.count('a') == 1
    rex = re.compile(opt)
    assert rex.match('a')
    assert rex.match('b')
    assert not rex.match('c')
    assert rex.groups == 1
