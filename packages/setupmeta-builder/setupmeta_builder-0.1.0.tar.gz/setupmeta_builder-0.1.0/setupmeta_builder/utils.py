# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import fsoopify
import re

def parse_homepage_from_git_url(git_url: str):
    'parse homepage url from a git url (or None if unable to parse)'

    # parse git@github.com:Cologler/setupmeta_builder-python.git
    # to https://github.com/Cologler/setupmeta_builder-python

    # parse https://github.com/Cologler/setupmeta_builder-python.git
    # to https://github.com/Cologler/setupmeta_builder-python

    match = re.match(r'^(?:(?:git\+)?(?:ssh|https)://)?(?:git@)?(?P<host>github.com)[\:/](?P<user>[^/]+)/(?P<repo>[^/\.]+)(?:\.git)?$', git_url)
    if match:
        host = match.group('host')
        user = match.group('user')
        repo = match.group('repo')
        return f'https://{host}/{user}/{repo}'
    return None

def get_global_funcnames(pyfile: fsoopify.FileInfo) -> list:
    'get a list of global funcnames (use for entry_points.console_scripts).'
    assert pyfile.is_file()

    import ast

    funcnames = []
    mod = ast.parse(pyfile.read_text())
    for stmt in mod.body:
        if isinstance(stmt, ast.FunctionDef):
            funcnames.append(stmt.name)
    return funcnames

def get_field(d: dict, path: str, default=None):
    '''
    example: get_field(pyproject, 'tool.poetry.version')
    '''

    parts = path.split('.')
    for field in parts[:-1]:
        d = d.get(field, {})
    return d.get(parts[-1], default)
