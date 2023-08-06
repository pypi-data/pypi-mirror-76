# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
from abc import abstractmethod, ABC
import os
import re

from packaging.requirements import Requirement

from .utils_poetry import get_requirements as poetry_get_requirements

class RequiresResolver(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    def resolve_install_requires(self, ctx) -> Optional[List[str]]:
        requires = self.parse_install_requires(ctx)
        if requires is not None:
            return [str(r) for r in requires]

    def resolve_tests_require(self, ctx) -> Optional[List[str]]:
        requires = self.parse_tests_require(ctx)
        if requires is not None:
            return [str(r) for r in requires]

    def resolve_extras_require(self, ctx) -> Optional[List[str]]:
        requires = self.parse_extras_require(ctx)
        if requires is not None:
            return dict(
                (n, [str(r) for r in rs]) for n, rs in requires.items()
            )

    def parse_install_requires(self, ctx) -> Optional[List[Requirement]]:
        return None

    def parse_tests_require(self, ctx) -> Optional[List[Requirement]]:
        return None

    def parse_extras_require(self, ctx) -> Optional[Dict[str, List[Requirement]]]:
        return None

    @staticmethod
    def _sorted_list(ls):
        return list(sorted(ls, key=lambda i: i.name))


class RequirementsTxtRequiresResolver(RequiresResolver):
    @property
    def name(self):
        return 'requirements.txt'

    @classmethod
    def _requirements_to_require(cls, requirements: str):
        requires = [Requirement(l) for l in requirements.splitlines() if l]
        return cls._sorted_list(requires)

    def parse_install_requires(self, ctx) -> list:
        requirements = ctx.get_text_content('requirements.txt')
        if requirements is None:
            return None

        return self._requirements_to_require(requirements)

    def parse_tests_require(self, ctx) -> list:
        return None

    def parse_extras_require(self, ctx) -> dict:
        root_path = str(ctx.root_path)
        file_names = os.listdir(root_path)
        extras_require = {}
        for fn in file_names:
            match = re.match(r'^requirements\.(?P<name>.+)\.txt$', fn, re.I)
            if match:
                extra_name = match['name']
                requirements = ctx.get_text_content(fn)
                extras_require[extra_name] = self._requirements_to_require(requirements)
        if extras_require:
            return extras_require


class PoetryRequiresResolver(RequiresResolver):
    @property
    def name(self):
        return 'poetry'

    def _get_dependencies(self, ctx, scope: str):
        pyproject = ctx.get_pyproject_conf()
        tool = pyproject.get('tool', {})
        poetry = tool.get('poetry', {})
        deps = poetry.get(scope, {})
        if deps:
            return deps

    def parse_install_requires(self, ctx) -> Optional[List[Requirement]]:
        datadict = self._get_dependencies(ctx, 'dependencies')
        if datadict:
            requirements = poetry_get_requirements(datadict)
            python_ver = requirements.pop('python', None) # currently ignore
            return list(requirements.values())

    def parse_tests_require(self, ctx) -> Optional[List[Requirement]]:
        datadict = self._get_dependencies(ctx, 'dev-dependencies')
        if datadict:
            requirements = poetry_get_requirements(datadict)
            python_ver = requirements.pop('python', None) # currently ignore
            return list(requirements.values())

    def parse_extras_require(self, ctx) -> Optional[Dict[str, List[Requirement]]]:
        return None


class PipfileRequiresResolver(RequiresResolver):
    @property
    def name(self):
        return 'Pipfile'

    def _get_pipfile(self, ctx):
        if 'pipfile' not in ctx.state:
            pipfile_path = ctx.root_path / 'Pipfile'
            if pipfile_path.is_file():
                import pipfile
                pf = pipfile.load(str(pipfile_path))
            else:
                pf = None
            ctx.state['pipfile'] = pf
        return ctx.state['pipfile']

    @staticmethod
    def _package_to_require(k, v):
        if v == '*':
            return Requirement(k)
        return Requirement(k+v)

    def _resolve_requires(self, ctx, attr_name, pf_key):
        pf = self._get_pipfile(ctx)
        if pf is None:
            return None
        requires = []
        for k, v in pf.data[pf_key].items():
            requires.append(self._package_to_require(k, v))
        return self._sorted_list(requires)

    def parse_install_requires(self, ctx) -> list:
        return self._resolve_requires(ctx, 'install_requires', 'default')

    def parse_tests_require(self, ctx) -> list:
        return self._resolve_requires(ctx, 'tests_require', 'develop')


class ChainRequiresResolver(RequiresResolver):
    def __init__(self, *resolvers):
        self.resolvers = list(resolvers)

    @property
    def name(self):
        childs_name = ', '.join([c.name for c in self.resolvers])
        return f'chain({childs_name})'

    def parse_install_requires(self, ctx) -> list:
        for r in self.resolvers:
            ret = r.resolve_install_requires(ctx)
            if ret is not None:
                return ret

    def parse_tests_require(self, ctx) -> list:
        for r in self.resolvers:
            ret = r.resolve_tests_require(ctx)
            if ret is not None:
                return ret

    def parse_extras_require(self, ctx) -> dict:
        for r in self.resolvers:
            ret = r.resolve_extras_require(ctx)
            if ret is not None:
                return ret


class StrictRequiresResolver(RequiresResolver):
    def __init__(self, *resolvers):
        self.resolvers = list(resolvers)

    @property
    def name(self):
        childs_name = ', '.join([c.name for c in self.resolvers])
        return f'strict({childs_name})'

    def _select_requirement(self, name, requirements):
        reqs = [i[1] for i in requirements]

        if len(reqs) > 1 and any(not r.specifier for r in reqs):
            reqs = [r for r in reqs if not r.specifier]

        if len(reqs) > 1:
            if len(set(str(req) for rsl, req in requirements)) == 1:
                # all same
                return reqs[0]
            reqs = [reqs[0]]

        if len(reqs) == 1:
            return reqs[0]

        msg = '\n'.join([
            f'{rsl.name} report: {req!r}' for rsl, req in requirements
        ])
        raise RuntimeError('different requirement from multi sources: \n' + msg)

    def _merge_results(self, rets: list):
        grouped_requirements = {}
        for resolver, requirements in rets:
            if requirements:
                for req in requirements:
                    grouped_requirements.setdefault(req.name, []).append((resolver, req))

        if grouped_requirements:
            rv = []
            for name in grouped_requirements:
                requirements = grouped_requirements[name]
                rv.append(self._select_requirement(name, requirements))
            return self._sorted_list(rv)

    def parse_install_requires(self, ctx) -> list:
        rets = [(r, r.parse_install_requires(ctx)) for r in self.resolvers]
        return self._merge_results(rets)

    def parse_tests_require(self, ctx) -> list:
        rets = [(r, r.parse_tests_require(ctx)) for r in self.resolvers]
        return self._merge_results(rets)

    def parse_extras_require(self, ctx) -> dict:
        rets = [(r, r.parse_extras_require(ctx)) for r in self.resolvers]
        return self._merge_results(rets)


class DefaultRequiresResolver(RequiresResolver):
    def __init__(self):
        self._install_resolver = StrictRequiresResolver(
            PoetryRequiresResolver(),
            RequirementsTxtRequiresResolver(),
            PipfileRequiresResolver()
        )
        self._test_resolver = StrictRequiresResolver(
            PoetryRequiresResolver(),
            PipfileRequiresResolver()
        )
        self._extras_resolver = StrictRequiresResolver(
            PoetryRequiresResolver(),
            RequirementsTxtRequiresResolver()
        )

    @property
    def name(self):
        return 'default'

    def parse_install_requires(self, ctx) -> list:
        return self._install_resolver.resolve_install_requires(ctx)

    def parse_tests_require(self, ctx) -> list:
        return self._test_resolver.resolve_tests_require(ctx)

    def parse_extras_require(self, ctx) -> dict:
        return self._extras_resolver.resolve_extras_require(ctx)
