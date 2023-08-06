# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .classifiers import IClassifierUpdater

LICENSE_MIT = 'MIT License'
LICENSE_APACHE_LICENSE_20 = 'Apache License 2.0'
LICENSE_GNU_GPL_2 = 'GNU GPLv2'
LICENSE_GNU_GPL_3 = 'GNU GPLv3'
LICENSE_GNU_AGPL_3 = 'GNU AGPLv3'
LICENSE_GNU_LGPL_2_1 = 'GNU LGPLv2.1'
LICENSE_GNU_LGPL_3 = 'GNU LGPLv3'
LICENSE_MPL_2 = 'Mozilla Public License 2.0'

_POETRY_LICENSE_MAPPING = {
    'Apache-2.0':           LICENSE_APACHE_LICENSE_20,
    'BSD-2-Clause':         None,
    'BSD-3-Clause':         None,
    'BSD-4-Clause':         None,
    'GPL-2.0-only':         LICENSE_GNU_GPL_2,
    'GPL-2.0-or-later':     None,
    'GPL-3.0-only':         LICENSE_GNU_GPL_3,
    'GPL-3.0-or-later':     None,
    'LGPL-2.1-only':        LICENSE_GNU_LGPL_2_1,
    'LGPL-2.1-or-later':    None,
    'LGPL-3.0-only':        LICENSE_GNU_LGPL_3,
    'LGPL-3.0-or-later':    None,
    'MIT':                  LICENSE_MIT,
}

def _build_licenses():
    d = {}
    cg = dict(globals())
    for name in cg:
        if name.startswith('LICENSE_'):
            d[cg[name]] = cg[name]
    return d

LICENSES = _build_licenses()

LICENSES.update({
    ('Apache License', 'Version 2.0, January 2004'): LICENSE_APACHE_LICENSE_20,
    ('GNU GENERAL PUBLIC LICENSE', 'Version 2, June 1991'): LICENSE_GNU_GPL_2,
    ('GNU GENERAL PUBLIC LICENSE', 'Version 3, 29 June 2007'): LICENSE_GNU_GPL_3,
    ('GNU AFFERO GENERAL PUBLIC LICENSE', 'Version 3, 19 November 2007'): LICENSE_GNU_AGPL_3,
    ('GNU LESSER GENERAL PUBLIC LICENSE', 'Version 2.1, February 1999'): LICENSE_GNU_LGPL_2_1,
    ('GNU LESSER GENERAL PUBLIC LICENSE', 'Version 3, 29 June 2007'): LICENSE_GNU_LGPL_3,
    'Mozilla Public License Version 2.0': LICENSE_MPL_2
})

LICENSES_CLASSIFIERS_MAP = {
    # see https://pypi.org/classifiers/
    LICENSE_MIT:                'License :: OSI Approved :: MIT License',
    LICENSE_APACHE_LICENSE_20:  'License :: OSI Approved :: Apache Software License',
    LICENSE_GNU_GPL_2:          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    LICENSE_GNU_GPL_3:          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    LICENSE_GNU_AGPL_3:         'License :: OSI Approved :: GNU Affero General Public License v3',
    LICENSE_GNU_LGPL_2_1:       'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    LICENSE_GNU_LGPL_3:         'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    LICENSE_MPL_2:              'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
}

def find_license_from_poetry(ctx):
    pyproject = ctx.get_pyproject_conf()
    tool = pyproject.get('tool', {})
    poetry = tool.get('poetry', {})
    license = tool.get('license', None)
    if license:
        return _POETRY_LICENSE_MAPPING.get(license)

def find_license_from_LICENSE(ctx):
    lice = ctx.get_text_content('LICENSE')
    if lice:
        lines = [l.strip() for l in lice.splitlines()] + ['', '']
        keys = (
            (lines[0], lines[1]),
            lines[0]
        )
        for key in keys:
            if key in LICENSES:
                return LICENSES[key]

def update_license(ctx):
    license = find_license_from_poetry(ctx) or \
              find_license_from_LICENSE(ctx)

    if license:
        ctx.setup_attrs.setdefault('license', license)

class LicenseClassifierUpdater(IClassifierUpdater):
    def update_classifiers(self, ctx, classifiers):
        lice = ctx.setup_attrs.get('license')
        if lice and lice in LICENSES_CLASSIFIERS_MAP:
            classifiers.append(
                LICENSES_CLASSIFIERS_MAP[lice]
            )
