# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008,2009 Fluendo, S.L.
# Copyright (C) 2010,2011 Flumotion Services, S.A.
# Copyright (C) 2012, Wouter Verhelst
# All rights reserved.
#
# This file may be distributed and/or modified under the terms of
# the GNU Lesser General Public License version 2.1 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.LGPL" in the source distribution for more information.
#
# Headers in this file shall remain intact.

import os
import gst
import io

from flumotion.component import feedcomponent
from flumotion.common import log, messages, errors
from flumotion.component.producers.firewire.firewire import Firewire
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import defer, reactor

__version__ = "$Rev$"


class DVswitchProvider(Firewire):
    def get_pipeline_template(self, properties):
        """ return the pipeline """
        return ('fdsrc name=fdsrc ! video/x-dv ! tee name=t'
                '    ! queue leaky=2 max-size-time=1000000000'
                '    ! dvdemux name=demux'
                '  demux. ! queue ! dvdec name=decoder'
                '    ! @feeder:video@'
                '  demux. ! queue ! audio/x-raw-int '
                '    ! volume name=setvolume'
                '    ! level name=volumelevel message=true '
                '    ! @feeder:audio@'
                '    t. ! queue ! @feeder:dv@')
    def _parse_aditional_properties(self, props):
        self.socketPath = props.get('path')
        self.socket = io.open(self.socketPath, 'rb', 0)

    def configure_pipeline(self, pipeline, properties):
        fdsrc = pipeline.get_by_name("fdsrc")
        fdsrc.props.fd = self.socket.fileno()
        Firewire.configure_pipeline(self, pipeline, properties)
