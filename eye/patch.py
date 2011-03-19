"""
YARRRRRRR!

Monkey-patch zope.interface so that unpickling interfaces that aren't
in the Python environment doesn't break.
"""

import zope.interface.declarations
from zope.interface.interface import InterfaceClass
from ZODB.broken import Broken

def patched_normalizeargs(sequence, output = None):
    """Normalize declaration arguments

    Normalization arguments might contain Declarions, tuples, or single
    interfaces.

    Anything but individial interfaces or implements specs will be expanded.
    """
    if output is None:
        output = []

    if Broken in getattr(sequence, '__bases__', ()):
        return [sequence]

    cls = sequence.__class__
    if InterfaceClass in cls.__mro__ or zope.interface.declarations.Implements in cls.__mro__:
        output.append(sequence)
    else:
        for v in sequence:
            patched_normalizeargs(v, output)

    return output

zope.interface.declarations._normalizeargs = patched_normalizeargs