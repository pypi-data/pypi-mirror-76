#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Conflict resolving value/counter implementations for use on persistent objects.

"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

import functools

from zope import interface

from zope.minmax._minmax import Maximum
from zope.minmax._minmax import Minimum
from zope.minmax._minmax import AbstractValue

from nti.zodb.interfaces import INumericValue
from nti.zodb.interfaces import INumericCounter
from nti.zodb.persistentproperty import PropertyHoldingPersistent

from six import integer_types

# Give all these things a 'set' method, a point for subclasses
# to potentially override
def _set(self, value):
    self.value = value
# catch incompatible changes
assert 'set' not in AbstractValue.__dict__ or AbstractValue.set is _set
AbstractValue.set = _set


@functools.total_ordering
@interface.implementer(INumericValue)
class AbstractNumericValue(AbstractValue): # pylint:disable=abstract-method
    """
    A numeric value that provides ordering operations.
    Defaults to zero.
    """
    value = 0

    def __init__(self, value=0):
        super(AbstractNumericValue, self).__init__(value)

    def increment(self, amount=1):
        self.set(self.value + amount)
        return self

    # Comparison methods
    def __eq__(self, other):
        try:
            return other is self or self.value == other.value
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.value < other.value
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.value > other.value
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __hash__(self):
        return self.value

    # Numeric methods
    def __isub__(self, other):
        other_value = getattr(other, 'value', other)
        self.set(self.value - other_value)
        return self

    def __iadd__(self, other):
        other_value = getattr(other, 'value', other)
        self.set(self.value + other_value)
        return self

    def __rsub__(self, other):
        # other - self.
        # By definition, not called if other is the same type as this
        return other - self.value

    def __add__(self, other):
        other_value = getattr(other, 'value', other)
        result = self.value + other_value
        if other_value is not other:
            result = type(self)(result)
        return result

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)


class _ConstantZeroValue(AbstractNumericValue):
    """
    Use this as a class attribute for a default values of zero. The
    value cannot be changed, and instances cannot be serialized.
    """

    def __init__(self, value=0):
        super(_ConstantZeroValue, self).__init__(value=0)
        assert 'value' not in self.__dict__

    def __getstate__(self):
        raise TypeError()

    def _p_resolveConflict(self, old, committed, new): # pylint:disable=arguments-differ
        raise NotImplementedError()

    def set(self, value):
        pass

    value = property(lambda s: 0, lambda s, nv: None)

    def increment(self, amount=1):
        raise NotImplementedError

_czv = _ConstantZeroValue()


def ConstantZeroValue(value=0):
    if value != 0:
        raise NotImplementedError
    return _czv
ConstantZeroValue.__doc__ = _ConstantZeroValue.__doc__


class NumericMaximum(AbstractNumericValue, Maximum):
    """
    Maximizes the number during conflicts.
    """
_SafeMaximum = NumericMaximum  # BWC


class NumericMinimum(AbstractNumericValue, Minimum):
    """
    Minimizes the number during conflicts.
    """


@interface.implementer(INumericCounter)
class MergingCounter(AbstractNumericValue):
    """
    A :mod:`zope.minmax` item that resolves conflicts by
    merging the numeric value of the difference in magnitude of changes.
    Intented to be used for monotonically increasing counters.

    As a special case, if the counter is reset to zero by both transactions,
    that becomes the new state.

    .. versionchanged:: 1.2.0
       Special case setting the counter to zero.

    """

    def increment(self, amount=1):
        assert amount >= 0
        self.value += amount
        return self

    def _p_resolveConflict(self, oldState, savedState, newState):  # pylint:disable=arguments-differ
        if savedState == newState == 0:
            return 0

        saveDiff = savedState - oldState
        newDiff = newState - oldState
        savedState = oldState + saveDiff + newDiff
        return savedState


class NumericPropertyDefaultingToZero(PropertyHoldingPersistent):
    """
    In persistent objects (that extend
    :class:`nti.zodb.persistentproperty.PersistentPropertyHolder`),
    use this to hold a merging counter or numeric minimum or maximum.

    This is a data descriptor::

        class Foo(PersistentPropertyHolder):

           a = NumericPropertyDefaultingToZero('a')

    """

    @interface.implementer(INumericCounter)
    class IncrementingZeroValue(_ConstantZeroValue):

        def __init__(self, name, holder, prop):
            _ConstantZeroValue.__init__(self)
            self.__name__ = name
            self.holder = holder
            self.prop = prop

        def increment(self, amount=1):
            # Use the original NumericPropertyDefaultingToZero descriptor
            # to set the value, calling the factory and storing it.
            self.prop.__set__(self.holder, amount)
            return self.prop.__get__(self.holder, type(self.holder))

        def set(self, value):
            if value == 0:
                return
            self.prop.__set__(self.holder, value)

        def _p_resolveConflict(self, *args):
            raise NotImplementedError

    as_number = False

    def __init__(self, name, factory, as_number=False):
        """
        Creates a new property in a new-style class that does not use ``__slots__``
        (persistent classes shouldn't use ``__slots__`` anyway).

        :param str name: The name of the property; this will be the key in the instance
                dictionary. This should match the name of the property
                (e.g., ``a = NumericPropertyDefaultingToZero( 'a',...)``) but is not required
                to. It must be a native string (bytes on py2, str/unicode on py3).
        :param callable factory: The value object factory that determines the type of
                conflict resolution used for this property. Typically :func:`NumericMaximum`,
                :class:`NumericMinimum` or :class:`MergingCounter`.
        :keyword bool as_number: If set to `True` (not the default), then
                when an instance reads this property, the numeric value will be returned;
                otherwise the ``factory`` class instance will be returned and you will
                want to access its ``.value`` attribute. Setting this property always
                takes the (raw) numeric value.
        """
        assert isinstance(name, str), "name must be native string"
        self.__name__ = name
        self.factory = factory
        if as_number:
            self.as_number = True

    def __activate(self, inst):
        """
        we must activate objects before accessing their dict otherwise it may not be loaded
        """
        try:
            inst._p_activate() # pylint:disable=protected-access
        except AttributeError:
            pass

    def __changed(self, inst):
        # sometimes instances are not actually persistent,
        # don't give them a _p_changed
        try:
            # pylint:disable=protected-access
            if not inst._p_changed:
                inst._p_changed = True
        except AttributeError:
            pass

    def __get__(self, inst, klass):
        if inst is None:
            return self

        self.__activate(inst)
        if self.__name__ in inst.__dict__:
            value = inst.__dict__[self.__name__]
            return value.value if self.as_number else value

        if self.as_number:
            return 0
        return self.IncrementingZeroValue(self.__name__, inst, self)

    def __set__(self, inst, value):
        self.__activate(inst)
        val = inst.__dict__.get(self.__name__, None)
        if val is None or isinstance(val, integer_types):
            if not value:
                # not in dict, but they gave us the default value, so ignore it
                return
            val = self.factory(value)
            inst.__dict__[self.__name__] = val
            self.__changed(inst)
            if getattr(inst, '_p_jar', None) is not None:
                inst._p_jar.add(val)
        else:
            val.set(value)

    def __delete__(self, inst):
        self.__activate(inst)
        if self.__name__ in inst.__dict__:
            del inst.__dict__[self.__name__]
            self.__changed(inst)
