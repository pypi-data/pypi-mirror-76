# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import re

from packaging.requirements import Requirement
from poetry.semver import parse_constraint

RE_AUTHORS = re.compile('^(?P<name>.+) <(?P<email>.+@.+)>$')

def parse_author(author: str) -> Tuple[str, str]:
    author = author.strip()
    match = RE_AUTHORS.match(author)
    if match:
        author_name, author_email = match.group('name'), match.group('email')
        return author_name, author_email
    return author, None

def get_requirements(items: dict) -> Dict[str, Requirement]:
    rv = {}
    for k, v in items.items():
        vc = None

        if isinstance(v, str):
            vc = parse_constraint(v)

        elif isinstance(v, dict):
            raise NotImplementedError

        else:
            raise TypeError(type(v))

        if vc:
            vcs = str(vc)
            if vcs == '*':
                rv[k] = Requirement(k)
            else:
                rv[k] = Requirement(k + vcs)

    return rv
