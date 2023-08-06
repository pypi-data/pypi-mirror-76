# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# all attrs from spec:
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
# ----------

import os
import json
import subprocess
from pathlib import Path
from collections import ChainMap

import fsoopify

from .consts import EXCLUDED_PACKAGES, SETUP_ATTRS
from .licenses import LICENSES
from .requires_resolver import DefaultRequiresResolver
from .version_resolver import update_version
from .utils import get_global_funcnames, get_field
from .utils_poetry import parse_author

class SetupAttrContext:
    _pkgit_conf: dict = None
    _pyproject_conf: dict = None

    def __init__(self, root_path=None):
        self._setup_attrs = {}
        self._root_path = Path(root_path) if root_path else Path.cwd()
        self._state = {}

    @property
    def setup_attrs(self):
        return self._setup_attrs

    @property
    def root_path(self):
        return self._root_path

    @property
    def state(self):
        '''
        a dict for store cached state.
        '''
        return self._state

    def get_fileinfo(self, relpath: str) -> fsoopify.FileInfo:
        '''get `FileInfo`.'''
        return fsoopify.FileInfo(str(self._root_path / relpath))

    def get_text_content(self, relpath: str) -> str:
        '''get file content or `None`'''
        fileinfo = self.get_fileinfo(relpath)
        if fileinfo.is_file():
            return fileinfo.read_text()

    def get_pkgit_conf(self) -> dict:
        if self._pkgit_conf is None:
            global_conf_path = Path.home() / '.pkgit.json'
            if global_conf_path.is_file():
                global_conf = json.loads(global_conf_path.read_text('utf-8'))
            else:
                global_conf = {}

            cwd_conf_text = self.get_text_content('.pkgit.json')
            if cwd_conf_text:
                cwd_conf = json.loads(cwd_conf_text)
            else:
                cwd_conf = {}

            self._pkgit_conf = ChainMap(cwd_conf, global_conf)

        return self._pkgit_conf

    def get_pyproject_conf(self) -> dict:
        if self._pyproject_conf is None:
            fileinfo = self.get_fileinfo('pyproject.toml')
            if fileinfo.is_file():
                self._pyproject_conf = fileinfo.load()
            else:
                self._pyproject_conf = {}

        return self._pyproject_conf

    def _run_git(self, argv: list):
        gitdir = str(self.root_path / '.git')
        argv = ['git', f'--git-dir={gitdir}'] + argv
        return subprocess.run(argv, encoding='utf-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


class SetupMetaBuilder:

    def __init__(self):
        self.requires_resolver = DefaultRequiresResolver()
        from .classifiers import IClassifierUpdater
        self.classifier_updaters = [
            cls() for cls in IClassifierUpdater.All
        ]

    def fill_ctx(self, ctx: SetupAttrContext):
        # resolve attr from setupmeta_builder auto detect
        for attr in SETUP_ATTRS:
            method = getattr(self, f'auto_{attr}', None)
            if method is not None and attr not in ctx.setup_attrs:
                method(ctx)

        # update attrs (like version etc)
        for attr in SETUP_ATTRS:
            method = getattr(self, f'update_{attr}', None)
            if method is not None:
                method(ctx)

        for attr in SETUP_ATTRS:
            method = getattr(self, f'post_{attr}', None)
            if method is not None:
                method(ctx)

    def auto_packages(self, ctx: SetupAttrContext):
        from setuptools import find_packages

        packages = find_packages(
            where=str(ctx.root_path),
            exclude=EXCLUDED_PACKAGES)
        ctx.setup_attrs['packages'] = packages

    def auto_py_modules(self, ctx: SetupAttrContext):
        # description:
        # https://packaging.python.org/guides/distributing-packages-using-setuptools/#py-modules
        #   If your project contains any single-file Python modules that aren’t part of a package,
        #   set py_modules to a list of the names of the modules (minus the .py extension)
        #   in order to make setuptools aware of them.

        packages = ctx.setup_attrs['packages']
        if packages:
            return # only discover if no packages.

        proj_name = ctx.root_path.name

        py_modules = []

        search_names = []
        search_names.append(proj_name)
        search_names.append(proj_name.replace('-', '_'))
        if proj_name.startswith('python-'):
            search_names.append(proj_name[len('python-'):])
        if proj_name.endswith('-python'):
            search_names.append(proj_name[:-len('-python')])
        for name in search_names:
            if ctx.get_fileinfo(f'{name}.py').is_file():
                py_modules.append(name)
                break

        if py_modules:
            ctx.setup_attrs['py_modules'] = py_modules

    def auto_long_description(self, ctx: SetupAttrContext):
        rst = ctx.get_text_content('README.rst')
        if rst is not None:
            ctx.setup_attrs['long_description'] = rst
            return

        md = ctx.get_text_content('README.md')
        if md is not None:
            ctx.setup_attrs['long_description'] = md
            ctx.setup_attrs['long_description_content_type'] = 'text/markdown'
            return

        ctx.setup_attrs.setdefault('long_description', '')

    def auto_name(self, ctx: SetupAttrContext):
        pyproject = ctx.get_pyproject_conf()
        tool = pyproject.get('tool', {})
        name = get_field(tool, 'poetry.name') or \
               get_field(tool, 'flit.metadata.module')

        if not name:
            def guess_name():
                packages = ctx.setup_attrs.get('packages', [])
                py_modules = ctx.setup_attrs.get('py_modules', [])
                sources = packages + py_modules
                if not sources:
                    raise RuntimeError(f'unable to parse name: no packages or py_modules found.')

                ns = set()
                for src in sources:
                    ns.add(src.partition('.')[0])
                if len(ns) > 1:
                    raise RuntimeError(f'unable to pick name from: {ns}')

                return list(ns)[0]
            name = guess_name()

        if name:
            ctx.setup_attrs['name'] = name

    def auto_version(self, ctx: SetupAttrContext):
        version = get_field(ctx.get_pyproject_conf(), 'tool.poetry.version')
        if version:
            ctx.setup_attrs.setdefault('version', version)

    def update_version(self, ctx: SetupAttrContext):
        update_version(ctx)

    def auto_author(self, ctx: SetupAttrContext):
        author_name = None
        author_email = None

        # parse from pyproject
        authors = get_field(ctx.get_pyproject_conf(), 'tool.poetry.authors', [])
        if authors:
            author_name, author_email = parse_author(authors[0])

        # parse from pkgit
        if author_name is None:
            author_name = ctx.get_pkgit_conf().get('author')

        if author_name:
            ctx.setup_attrs['author'] = author_name
        if author_email:
            ctx.setup_attrs.setdefault('author_email', author_email)

    def auto_author_email(self, ctx: SetupAttrContext):
        author_email = ctx.get_pkgit_conf().get('author_email')
        if author_email:
            ctx.setup_attrs['author_email'] = author_email

    def auto_url(self, ctx: SetupAttrContext):
        def get_url_from_remote(name):
            git_remote_get_url = ctx._run_git(['remote', 'get-url', name])
            if git_remote_get_url.returncode != 0:
                return
            return git_remote_get_url.stdout.strip()

        git_remote = ctx._run_git(['remote'])
        if git_remote.returncode != 0:
            return
        lines = git_remote.stdout.strip().splitlines()
        if 'origin' in lines:
            git_url = get_url_from_remote('origin')
        else:
            git_url = None

        if git_url:
            from .utils import parse_homepage_from_git_url
            url = parse_homepage_from_git_url(git_url)
            if url:
                ctx.setup_attrs['url'] = url

    def auto_license(self, ctx: SetupAttrContext):
        from .licenses import update_license
        update_license(ctx)

    def auto_scripts(self, ctx: SetupAttrContext):
        pass

    def auto_entry_points(self, ctx: SetupAttrContext):
        entry_points = {}
        console_scripts = self._get_entry_points_console_scripts(ctx)
        if console_scripts:
            entry_points['console_scripts'] = console_scripts
        ctx.setup_attrs['entry_points'] = entry_points

    def _get_entry_points_console_scripts(self, ctx: SetupAttrContext):
        name = ctx.setup_attrs.get('name')
        console_scripts = []
        if name:
            csf = ctx.get_fileinfo(os.path.join(name, 'entry_points_console_scripts.py'))
            if csf.is_file():
                for fn in get_global_funcnames(csf):
                    if not fn.startswith('_'):
                        script_name = fn.replace('_', '-')
                        console_scripts.append(
                            f'{script_name}={name}.entry_points_console_scripts:{fn}'
                        )
        return console_scripts

    def auto_zip_safe(self, ctx: SetupAttrContext):
        ctx.setup_attrs['zip_safe'] = False

    def auto_include_package_data(self, ctx: SetupAttrContext):
        ctx.setup_attrs['include_package_data'] = True

    def auto_setup_requires(self, ctx: SetupAttrContext):
        pass

    def auto_install_requires(self, ctx: SetupAttrContext):
        requires = self.requires_resolver.resolve_install_requires(ctx)
        if requires is not None:
            ctx.setup_attrs['install_requires'] = requires

    def auto_tests_require(self, ctx: SetupAttrContext):
        requires = self.requires_resolver.resolve_tests_require(ctx)
        if requires is not None:
            ctx.setup_attrs['tests_require'] = requires

    def auto_extras_require(self, ctx: SetupAttrContext):
        requires = self.requires_resolver.resolve_extras_require(ctx)
        if requires is not None:
            ctx.setup_attrs['extras_require'] = requires

    def post_classifiers(self, ctx: SetupAttrContext):
        # see: https://pypi.org/classifiers/
        classifiers = ctx.setup_attrs.get('classifiers', [])

        for updater in self.classifier_updaters:
            updater.update_classifiers(ctx, classifiers)

        ctx.setup_attrs['classifiers'] = list(sorted(set(classifiers)))
