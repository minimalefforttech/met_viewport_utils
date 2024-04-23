# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
from __future__ import annotations
class _ext:
    """ External Dependencies """
    from dataclasses import dataclass

@_ext.dataclass
class Margins:
    left:int = 0
    top:int = 0
    right:int = 0
    bottom:int = 0

    def __len__(self):
        return 4
    
    def __iter__(self):
        return iter((
            self.left,
            self.top,
            self.right,
            self.bottom
        ))
    
    def __bool__(self):
        return any(self)
    
    def inverse(self)->Margins:
        return Margins(-self.left, -self.top, -self.right, -self.bottom)