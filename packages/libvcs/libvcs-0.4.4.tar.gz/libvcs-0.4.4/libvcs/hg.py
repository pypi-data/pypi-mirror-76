# -*- coding: utf-8 -*-
"""Mercurial Repo object for libvcs.

libvcs.hg
~~~~~~~~~

The following is from pypa/pip (MIT license):

- :py:meth:`MercurialRepo.get_url_and_revision_from_pip_url`
- :py:meth:`MercurialRepo.get_url`
- :py:meth:`MercurialRepo.get_revision`

"""
from __future__ import absolute_import, print_function, unicode_literals

import logging
import os

from .base import BaseRepo

logger = logging.getLogger(__name__)


class MercurialRepo(BaseRepo):
    bin_name = 'hg'
    schemes = ('hg', 'hg+http', 'hg+https', 'hg+file')

    def __init__(self, url, **kwargs):
        BaseRepo.__init__(self, url, **kwargs)

    def obtain(self):
        self.check_destination()

        self.run(['clone', '--noupdate', '-q', self.url, self.path])
        self.run(['update', '-q'])

    def get_revision(self):
        return self.run(['parents', '--template={rev}'])

    def update_repo(self):
        self.check_destination()
        if not os.path.isdir(os.path.join(self.path, '.hg')):
            self.obtain()
            self.update_repo()
        else:
            self.run(['update'])
            self.run(['pull', '-u'])
