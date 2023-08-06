# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .classifiers import IClassifierUpdater
from packaging.version import Version, parse

def _parse_strict_version(ctx, tag):
    ver = parse(tag)
    if isinstance(ver, Version):
        ctx.state[Version] = ver
        return str(ver)

def update_version(ctx):
    git_describe = ctx._run_git(['describe', '--tags'])
    if git_describe.returncode != 0:
        return
    describe_info: str = git_describe.stdout.strip()
    tag = describe_info.split('-')[0]
    ver = _parse_strict_version(ctx, tag)
    if ver:
        ctx.setup_attrs['version'] = ver

class VersionClassifierUpdater(IClassifierUpdater):
    CLASSIFIER_PLANNING = 'Development Status :: 1 - Planning'
    CLASSIFIER_PRE_ALPHA = 'Development Status :: 2 - Pre-Alpha'
    CLASSIFIER_ALPHA = 'Development Status :: 3 - Alpha'
    CLASSIFIER_BETA = 'Development Status :: 4 - Beta'
    CLASSIFIER_STABLE = 'Development Status :: 5 - Production/Stable'
    CLASSIFIER_MATURE = 'Development Status :: 6 - Mature'
    CLASSIFIER_INACTIVE = 'Development Status :: 7 - Inactive'

    def update_classifiers(self, ctx, classifiers):
        version = ctx.state.get(Version)

        if version is not None:
            if version.is_devrelease:
                classifiers.append(self.CLASSIFIER_PRE_ALPHA)

            elif version.is_postrelease:
                classifiers.append(self.CLASSIFIER_ALPHA)

            elif version.is_prerelease:
                classifiers.append(self.CLASSIFIER_BETA)

            else:
                classifiers.append(self.CLASSIFIER_STABLE)
