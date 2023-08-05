#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# pylint: disable=protected-access
import unittest
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import has_length
from hamcrest import is_
from hamcrest import contains_exactly

from zope.testing.loggingsupport import InstalledHandler

from nti.zodb.activitylog import AbstractActivityMonitor as ActivityMonitor
from nti.zodb.activitylog import LogActivityMonitor
from nti.zodb.activitylog import LogActivityComponent
from nti.zodb.activitylog import StatsdActivityMonitor
from nti.zodb.activitylog import StatsdActivityComponent
from nti.zodb.activitylog import ActivityMonitorData

AM_DATA = ActivityMonitorData(1, 1, 'foo', 42, 5)

class TestBase(unittest.TestCase):

    def test_delegate_properties(self):

        class Base(object):
            b = 1

        base = Base()
        mon = ActivityMonitor(base)

        assert_that(mon, has_property('b', 1))

    def test_closedConnection(self):
        from ZODB import DB
        from ZODB.DemoStorage import DemoStorage
        class Conn(DB.klass):
            loads = 1
            stores = 2

            def db(self):
                return db
            def getTransferCounts(self, clear=False):
                l, s = self.loads, self.stores
                if clear:
                    self.loads = self.stores = 0
                return l, s

        class MyDB(DB):
            klass = Conn

        db = MyDB(DemoStorage())
        database_name = 'DB'
        db.database_name = database_name
        self.addCleanup(db.close)

        db.klass = Conn

        called_component = []
        def component(data):
            called_component.append(1)
            assert_that(data.loads, is_(1))
            assert_that(data.stores, is_(2))
            assert_that(data.db_name, is_(database_name))
            assert_that(data.pool_all_count, is_(1))
            assert_that(data.pool_idle_count, is_(0))

        mon = ActivityMonitor(components=[component])
        conn = db.open()
        self.addCleanup(conn.close)

        mon.closedConnection(conn)

        assert_that(conn.loads, is_(0))
        assert_that(conn.stores, is_(0))
        assert_that(called_component, is_([1]))

class TestLogActivityMonitor(unittest.TestCase):

    def setUp(self):
        super(TestLogActivityMonitor, self).setUp()
        self.handler = InstalledHandler('nti.zodb.activitylog')
        self.addCleanup(self.handler.uninstall)

    def test_closed_connection(self):
        mon = LogActivityMonitor()
        mon.components[0](AM_DATA)

        assert_that(self.handler.records, has_length(1))

    def test_closed_connection_threshold(self):
        mon = LogActivityMonitor()
        mon.components[0].min_loads_and_stores = 3
        mon.components[0](AM_DATA)

        assert_that(self.handler.records, has_length(0))


class TestStatsdLogActivityMonitor(unittest.TestCase):

    def test_closed_connection_no_client(self):
        mon = StatsdActivityMonitor()
        mon.statsd_client = lambda: None
        assert_that(mon.components[0], is_(StatsdActivityComponent))
        mon.components[0](AM_DATA)

    def test_closed_connection_with_client(self):
        glob_buf = []
        class MockClient(object):
            def gauge(self, key, value, buf):
                buf.append((key, value))
            def sendbuf(self, buf):
                glob_buf.extend(buf)

        mon = StatsdActivityComponent()
        mon.statsd_client = MockClient
        mon(AM_DATA)
        assert_that(glob_buf, is_([
            ('ZODB.DB.foo.loads', 1),
            ('ZODB.DB.foo.stores', 1),
            ('ZODB.DB.foo.total_connections', 42),
            ('ZODB.DB.foo.idle_connections', 5),
        ]))

class TestRegisterSubscriber(unittest.TestCase):

    def test_execute(self):
        from zope.processlifetime import DatabaseOpenedWithRoot
        from nti.zodb.activitylog import register_subscriber
        from nti.zodb.activitylog import ComponentActivityMonitor

        class DB(object):
            dam = None

            def __init__(self):
                self.databases = {'': self}
            def getActivityMonitor(self):
                return self.dam

            def setActivityMonitor(self, dam):
                self.dam = dam

        db = DB()
        db.setActivityMonitor(42)
        event = DatabaseOpenedWithRoot(db)

        register_subscriber(event)

        dam = db.getActivityMonitor()
        assert_that(dam, is_(ComponentActivityMonitor))
        assert_that(dam, has_property('base', is_(42)))
        assert_that(dam, has_property(
            'components',
            contains_exactly(is_(LogActivityComponent),
                             is_(StatsdActivityComponent))))
