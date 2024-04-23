# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
from __future__ import annotations
class _ext:
    """ External Dependencies """
    from met_viewport_utils.algorithm.meta import typed_property
    import abc

class INameItem(_ext.abc.ABC):
    """Indicates item has a name property"""
    name:str = _ext.typed_property(str, "untitled")
