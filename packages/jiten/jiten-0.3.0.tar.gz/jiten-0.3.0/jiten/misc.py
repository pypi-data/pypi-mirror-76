#!/usr/bin/python3
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : jiten/misc.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2020-08-07
#
# Copyright   : Copyright (C) 2020  Felix C. Stegerman
# Version     : v0.2.0
# License     : AGPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""

Miscellaneous helper functions.

>>> ishiragana("ふ"), ishiragana("フ")
(True, False)
>>> iskatakana("ふ"), iskatakana("フ")
(False, True)

>>> iskana("ふ"), iskana("フ")
(True, True)

>>> iskanji("猫")
True

>>> ispunc("々")
True

>>> list(flatten([[1, 2], [3, 4]]))
[1, 2, 3, 4]

>>> list(uniq([1, 2, 3, 1, 4, 2, 2]))
[1, 2, 3, 4]

"""                                                             # }}}1

import itertools, os, sys

class RegexError(RuntimeError): pass

OKPUNC      = "々"

ispunc      = lambda c:  0x3000 <= ord(c) <=  0x303f
ishiragana  = lambda c:  0x3040 <= ord(c) <=  0x309f
iskatakana  = lambda c:  0x30a0 <= ord(c) <=  0x30ff

iskanji     = lambda c:  0x4e00 <= ord(c) <=  0x9fff
iscompat    = lambda c:  0xf900 <= ord(c) <=  0xfaff
isuniext    = lambda c:  0x3400 <= ord(c) <=  0x4dbf or \
                        0x20000 <= ord(c) <= 0x2ebef

isradical   = lambda c:  0x2e80 <= ord(c) <=  0x2eff or \
                         0x2f00 <= ord(c) <=  0x2fdf

iskana      = lambda c: ishiragana(c) or iskatakana(c)
isideo      = lambda c: iskanji(c) or iscompat(c) or isuniext(c)
isjap       = lambda c: iskanji(c) or iskana(c)                 # TODO
isokjap     = lambda c: isjap(c) or c in OKPUNC                 # TODO
iscjk       = lambda c: isideo(c) or iskana(c) or ispunc(c)     # TODO

flatten     = itertools.chain.from_iterable

def uniq(xs):
  seen = set()
  for x in xs:
    if x not in seen:
      seen.add(x); yield x

# TODO: use importlib.resources?!
def resource_path(path):
  return os.path.join(os.path.dirname(__file__), *path.split("/"))

def process_query(q, word, exact, fstwd):
  if not q: return ""
  q = q.strip()
  if q.startswith("+"): return q
  if exact: return "^"   + q +   "$"
  if fstwd: return "^"   + q + "\\b"
  if word : return "\\b" + q + "\\b"
  return q

def q2rx(q):
  return "(?im)" + q

if __name__ == "__main__":
  if "--doctest" in sys.argv:
    verbose = "--verbose" in sys.argv
    import doctest
    if doctest.testmod(verbose = verbose)[0]: sys.exit(1)

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
