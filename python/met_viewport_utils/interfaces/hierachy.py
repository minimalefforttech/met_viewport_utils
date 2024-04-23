# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
from __future__ import annotations
class _ext:
    """ External Dependencies """
    import weakref
    from typing import List, Union
    from collections import deque
    from met_viewport_utils.algorithm.meta import typed_property
    from .name import INameItem


class IHierarchyItem(_ext.INameItem):
    """Indicates item has parent and children properties"""
    def __init__(self):
        self.name:str = None
        self._parent:IHierarchyItem = None
        self.children:_ext.List[IHierarchyItem] = []
    
    name:str = _ext.typed_property(str, "")
    
    @property
    def parent(self):
        if self._parent:
            return self._parent()
        return None
    
    @parent.setter
    def parent(self, item:_ext.Union[IHierarchyItem, None]):
        current_parent = self.parent
        if current_parent:
            if self in current_parent.children:
                current_parent.children.remove(self)
        if item:
            self._parent = _ext.weakref.ref(item)
            if self not in item.children:
                item.children.append(self)
        else:
            self._parent = None
    
    @property
    def path(self):
        names = _ext.deque([self.name])
        parent = self.parent
        while parent:
            names.appendleft(parent.name)
            parent = parent.parent
        
        return "/" + "/".join(names)
    
    def append(self, children:_ext.Union[IHierarchyItem, _ext.List[IHierarchyItem]]):
        if isinstance(children, IHierarchyItem):
            children = [children]
            
        children = [child for child in children if child not in self.children]
        self.children += children
        for child in children:
            child.parent = self

    def insert(self, index:int, children:_ext.Union[IHierarchyItem, _ext.List[IHierarchyItem]]):
        if isinstance(children, IHierarchyItem):
            children = [children]
            
        children = [child for child in children if child not in self.children]
        self.children[index:index] = children
        for child in children:
            child.parent = self
    
    def clear(self):
        """Remove all children"""
        for child in self.children:
            child.parent = None
        
        self.children = []

    def get_root(self)->IHierarchyItem:
        parent = self.parent
        if not parent:
            return self
        while parent.parent:
            parent = parent.parent
        return parent

    def iter_descendants(self, type=None):
        """ Recurse children based on an instance check
        This allows to check for class instances that may have non class type parents
        """
        for child in self.children:
            if type is None or isinstance(child, type):
                prune = yield child
                if prune:
                    continue
            
            generator = child.iter_descendants(type)
            for each in generator:
                prune = yield each
                if prune:
                    generator.send(prune)

    def iter_parents(self, type=None):
        """ Recurse parents based on an instance check
        This allows to check for class instances that may have non class type parents
        """
        parent = self.parent
        while parent:
            if type is None or isinstance(parent, type):
                yield parent
            parent = parent.parent
