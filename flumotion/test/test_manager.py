# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Flumotion - a video streaming server
# Copyright (C) 2004 Fluendo
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Street #330, Boston, MA 02111-1307, USA.

from twisted.trial import unittest

from flumotion.manager import component, manager

class FakeComponentAvatar:
    def __init__(self, name='fake', eaters=[], port=-1, listen_host='listen-host'):
        self.name = name
        self.eaters = eaters
        self.port = port
        self.listen_host = listen_host
        
    def getFeeders(self, long):
        if long:
            return [self.name + ':default']
        else:
            return ['default']

    def getEaters(self):
        return self.eaters
    
    def getListenHost(self):
        return self.listen_host

    def getListenPort(self, *args):
        return self.port
    
    def getTransportPeer(self):
        return 0, '127.0.0.1', 0

    def getName(self):
        return self.name

class TestComponentHeaven(unittest.TestCase):
    def setUp(self):
        self.heaven = component.ComponentHeaven(manager.Vishnu())

    def testCreateAvatar(self):
        p = self.heaven.createAvatar('foo-bar-baz')
        assert isinstance(p, component.ComponentAvatar)

        #self.assertRaises(AssertionError,
        #                  self.heaven.createAvatar, 'does-not-exist')

    def testIsLocalComponent(self):
        a = FakeComponentAvatar()
        self.heaven._addAvatar(a)
        assert self.heaven.isLocalComponent(a)
        
    def testIsStarted(self):
        a = self.heaven.createAvatar('prod')
        assert not self.heaven.isComponentStarted('prod')
        a.started = True # XXX: Use heaven.componentStart
        assert self.heaven.isComponentStarted('prod')

    def testGetComponent(self):
        a = self.heaven.createAvatar('prod')
        assert self.heaven.getComponent('prod') == a

    def testHasComponent(self):
        a = self.heaven.createAvatar('prod')
        assert self.heaven.hasComponent('prod')
        self.heaven.removeComponent(a)
        assert not self.heaven.hasComponent('prod')
        self.assertRaises(KeyError, self.heaven.removeComponent, a)
        
    def testAddComponent(self):
        a = FakeComponentAvatar('fake')
        self.heaven._addAvatar(a)
        assert self.heaven.hasComponent('fake')
        self.assertRaises(KeyError, self.heaven._addAvatar, a)
        
    def testRemoveComponent(self):
        assert not self.heaven.hasComponent('fake')
        a = FakeComponentAvatar('fake')
        self.assertRaises(KeyError, self.heaven.removeComponent, a)
        self.heaven._addAvatar(a)
        assert self.heaven.hasComponent('fake')
        self.heaven.removeComponent(a)
        assert not self.heaven.hasComponent('fake')
        self.assertRaises(KeyError, self.heaven.removeComponent, a)

    def testComponentEatersEmpty(self):
        a = FakeComponentAvatar('fake')
        self.heaven._addAvatar(a)
        assert self.heaven.getComponentEaters(a) == []
        
    def testComponentsEaters(self):
        a = FakeComponentAvatar('foo', ['bar', 'baz'])
        self.heaven._addAvatar(a)
        a2 = FakeComponentAvatar('bar', port=1000, listen_host='bar-host')
        self.heaven._addAvatar(a2)
        a3 = FakeComponentAvatar('baz', port=1001, listen_host='baz-host')
        self.heaven._addAvatar(a3)
        self.heaven.feeder_set.addFeeders(a2)
        self.heaven.feeder_set.addFeeders(a3)
        
        eaters = self.heaven.getComponentEaters(a)
        assert len(eaters) == 2
        assert ('bar', 'bar-host', 1000) in eaters
        assert ('baz', 'baz-host', 1001) in eaters        

if __name__ == '__main__':
     unittest.main()
