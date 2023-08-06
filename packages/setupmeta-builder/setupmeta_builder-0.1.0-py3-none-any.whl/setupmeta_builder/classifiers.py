# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# see: https://pypi.org/classifiers/
# ----------

from abc import abstractmethod, ABC

PY_CLASSIFIERS_MAP = {
    '2': 'Programming Language :: Python :: 2',
    '3': 'Programming Language :: Python :: 3',
}

def _init_py_classifiers_map():
    # add 2.x
    for sub_ver in range(3, 8):
        PY_CLASSIFIERS_MAP[f'2.{sub_ver}'] = f'Programming Language :: Python :: 2.{sub_ver}'

    # add 3.x
    for sub_ver in range(0, 10):
        PY_CLASSIFIERS_MAP[f'3.{sub_ver}'] = f'Programming Language :: Python :: 3.{sub_ver}'

_init_py_classifiers_map()

class IClassifierUpdater(ABC):
    All = []

    @abstractmethod
    def update_classifiers(self, ctx, classifiers: list):
        raise NotImplementedError

    def __init_subclass__(cls, *args, **kwargs):
        cls.All.append(cls)


class TravisCIClassifierUpdater(IClassifierUpdater):
    def update_classifiers(self, ctx, classifiers: list):
        # see: https://pypi.org/classifiers/
        travis_yaml = ctx.get_fileinfo('.travis.yml')
        if travis_yaml.is_file():
            travis_conf = travis_yaml.load(format='yaml')
            pylist = travis_conf.get('python', [])
            for py in pylist:
                if py in PY_CLASSIFIERS_MAP:
                    classifiers.append(PY_CLASSIFIERS_MAP[py])
