#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Logging of database connection activity. Activate this with ZCML::

    <include package="nti.zodb" file="configure_activitylog.zcml" />

Originally based on code from the unreleased zc.zodbactivitylog.

"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from collections import namedtuple
from functools import partial
from perfmetrics import statsd_client

logger = __import__('logging').getLogger(__name__)

class ComponentActivityMonitor(object):
    """
    Activity monitor that:

    - Can call another activity monitor; this is useful for adding
      on to an existing activity monitor.
    - Can call a sequence of callables with some data. This is useful for
      composing many activity monitors much more cheaply than if they
      were on their own.
    """

    __slots__ = (
        'base',
        'components',
        '_get_loads_stores',
    )

    def __init__(self, base=None, components=()):
        """
        :param base: An arbitrary activity monitor.
        :param components: An iterable of :class:`ActivityMonitorComponent`
           instances (callables taking a :class:`ActivityMonitorData`).
        """
        self.base = base
        self.components = components
        if base is not None:
            self._get_loads_stores = partial(self._call_base_get_loads_stores, base)
        else:
            self._get_loads_stores = self._no_base_get_loads_stores

    @staticmethod
    def _call_base_get_loads_stores(base, conn):
        # Capture the load and store counts before the base has a
        # chance to clear them.
        loads, stores = conn.getTransferCounts(False)
        base.closedConnection(conn)
        # Make sure connection counts are cleared if the base did not.
        conn.getTransferCounts(True)
        return loads, stores

    @staticmethod
    def _no_base_get_loads_stores(conn):
        # We're the end of the chain, we can clear
        return conn.getTransferCounts(True)

    def closedConnection(self, conn):
        # This is called for every transaction, so performance matters somewhat.
        # OTOH, what we do here is probably far less costly than writing a log message;
        # the Statsd client from perfmetrics buffers so it's pretty cheap.
        # Still, we expect most people to use both statsd and logging, so doing some work
        # a single time should pay off.
        db = conn.db()
        db_name = db.database_name
        # These are both usually protected by a lock as they can mutate together.
        # We're not really concerned about that. We use `len`, implemented in C, which
        # doesn't drop the GIL, so we're also not concerned about mutation happening while
        # we iterate.
        pool_all_count = len(db.pool.all)
        pool_available_count = len(db.pool.available)
        loads, stores = self._get_loads_stores(conn)
        data = ActivityMonitorData(loads, stores, db_name, pool_all_count, pool_available_count)
        for component in self.components:
            component(data)

    def __getattr__(self, name):
        return getattr(self.base, name)

AbstractActivityMonitor = ComponentActivityMonitor # BWC

#: The data passed to :class:`ActivityMonitorComponent`
ActivityMonitorData = namedtuple('ActivityMonitorData',
                                 ('loads', 'stores', 'db_name',
                                  'pool_all_count', 'pool_idle_count'))

class ActivityMonitorComponent(object):
    """
    One component of a chain of activity monitors.
    """

    __slots__ = ()

    def __call__(self, data):
        """
        Called when a connection has been closed.

        :param ActivityMonitorData data: An instance of `ActivityMonitorData`.
        """

class LogActivityComponent(ActivityMonitorComponent):
    """
    An activity monitor component that logs connection transfer information
    and pool information.
    """

    #: Only perform the logging if the total of loads + stores is
    #: at least this many.
    min_loads_and_stores = 1

    def __call__(self, data):
        # type: (ActivityMonitorData) -> None
        if data.loads + data.stores >= self.min_loads_and_stores:
            logger.info(
                "closedConnection={'loads': %5d, 'stores': %5d, 'database': %s, "
                "'num_connections': %5d, 'num_avail_connections': %5d}",
                data.loads, data.stores, data.db_name,
                data.pool_all_count, data.pool_idle_count)


class LogActivityMonitor(ComponentActivityMonitor):
    """
    A pre-configured :class:`ComponentActivityMonitor` that uses
    :func:`LogActivityComponent`
    """

    def __init__(self, base=None):
        ComponentActivityMonitor.__init__(self, base, (LogActivityComponent(),))


class StatsdActivityComponent(ActivityMonitorComponent):
    """
    An activity monitor component that stores counters (guages) in statsd,
    if the statsd client is available.

    The stats are:

    - ZODB.DB.<name>.loads
      How many loads the open connection performed.
    - ZODB.DB.<name>.stores
      How many stores the open connection performed.
    - ZODB.DB.<name>.total_connections
      All currently open connections, including those in use
      and those in the pool.
    - ZODB.DB.<name>.available_connections
      The connections sitting idle in the pool.
    """

    statsd_client = staticmethod(statsd_client)

    def __call__(self, data):
        # type: (ActivityMonitorData) -> None
        statsd = self.statsd_client()
        if statsd is None:
            return

        # Should these be counters or gauges? Or even sets?
        # counters are aggregated across all instances, gauges (by default) are broken out
        # by host
        buf = []
        statsd.gauge('ZODB.DB.' + data.db_name + '.loads',
                     data.loads, buf=buf)
        statsd.gauge('ZODB.DB.' + data.db_name + '.stores',
                     data.stores, buf=buf)
        statsd.gauge('ZODB.DB.' + data.db_name + '.total_connections',
                     data.pool_all_count, buf=buf)
        statsd.gauge('ZODB.DB.' + data.db_name + '.idle_connections',
                     data.pool_idle_count, buf=buf)
        statsd.sendbuf(buf)


class StatsdActivityMonitor(ComponentActivityMonitor):
    """
    A pre-configured :class:`ComponentActivityMonitor` that uses
    :func:`LogActivityComponent`
    """

    def __init__(self, base=None):
        ComponentActivityMonitor.__init__(self, base, (StatsdActivityComponent(),))


def register_subscriber(event):
    """
    Subscriber to the :class:`zope.processlifetime.IDatabaseOpenedWithRoot`
    that registers an activity monitor.
    """
    # IDatabaseOpened fires for each database, so if we sub to that we'd do this many times.
    # WithRoot fires only once.
    for database in event.database.databases.values():
        monitor = ComponentActivityMonitor(
            database.getActivityMonitor(),
            [LogActivityComponent(), StatsdActivityComponent()]
        )
        database.setActivityMonitor(monitor)
