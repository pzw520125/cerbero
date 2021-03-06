# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os

from cerbero.bootstrap import BootstrapperBase
from cerbero.bootstrap.bootstrapper import register_bootstrapper
from cerbero.config import Distro
from cerbero.utils import shell

CPANM_VERSION = '1.7044'
CPANM_URL_TPL = 'https://raw.githubusercontent.com/miyagawa/cpanminus/{}/cpanm'
CPANM_CHECKSUM = '22b92506243649a73cfb55c5990cedd24cdbb20b15b4530064d2496d94d1642b'

class OSXBootstrapper (BootstrapperBase):


    def __init__(self, config, offline, assume_yes):
        super().__init__(config, offline)
        url = CPANM_URL_TPL.format(CPANM_VERSION)
        self.fetch_urls.append((url, CPANM_CHECKSUM))

    def start(self, jobs=0):
        # skip system package install if not needed
        if not self.config.distro_packages_install:
            return
        self._install_perl_deps()

    def _install_perl_deps(self):
        cpanm_installer = os.path.join(self.config.local_sources, 'cpanm')
        shell.call('chmod +x %s' % cpanm_installer)
        # Install XML::Parser, required for intltool
        shell.call("sudo %s XML::Parser" % cpanm_installer)


def register_all():
    register_bootstrapper(Distro.OS_X, OSXBootstrapper)
