# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
from __future__ import annotations
class _ext:
    """ External Dependencies """
    import logging
    LOGGER = logging.getLogger("met_viewport_utils.gpu.font")
    import abc
    from typing import Union
    try:
        # TODO: Replace matplotlib, not using anything else from it
        from matplotlib import font_manager
    except ImportError:
        LOGGER.warning("Failed to import matplotlib, cannot set fonts")
    from pathlib import Path
    from met_viewport_utils.algorithm.meta import typed_property
    from met_viewport_utils.constants import FontStyle, FontWeight, Align
    from met_viewport_utils.algorithm.color import parse_color
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.algorithm import types
    from .viewport import IViewport
LOGGER = _ext.LOGGER

class IGPUFont(_ext.abc.ABC):
    """ Convenience class for drawing text to screen
    
    Properties:
        path(Path): Path to font file
        
        family(str)
        weight(FontWeight)
        style(FontStyle)
        align(Align)
        path(Path)
        
        color(Vector)
        shadow_color(Vector)
        shadow_offset(Vector)
        shadow_blur(int)
        point_size(int)
        angle(float)
    """
    _updating = False  # If bulk updating values, suppress load
                
    def copy(self)->IGPUFont:
        """ Return a copy of this font"""
        copy:IGPUFont = self.__class__()
        
        copy._updating = True
        try:
            copy.family = self.family
            copy.weight = self.weight
            copy.style = self.style
            copy.align = self.align
            copy.path = self.path
            
            copy.color = self.color
            copy.shadow_color = self.shadow_color
            copy.shadow_offset = self.shadow_offset
            copy.shadow_blur = self.shadow_blur
            copy.point_size = self.point_size
            copy.angle = self.angle
        finally:
            copy._updating = False
        return copy
            
    
    @classmethod
    def from_path(cls, path:_ext.Union[str, _ext.Path])->IGPUFont:
        """Initialize from a path

        Args:
            path ([str, _ext.Path]): Path to font file

        Returns:
            IGPUFont
        """
        config = cls()
        config._updating = True
        try:
            config.path = _ext.Path(path)
            # TODO: Determine from path, do we even use these?
            config.family = "unknown"
            config.weight = _ext.FontWeight.Unknown
            config.style = _ext.FontStyle.Unknown
        finally:
            config._updating = False
        config._load()
        return config
    
    @classmethod
    def from_props(cls, family:str, style:_ext.FontStyle=_ext.FontStyle.Normal, weight:_ext.FontWeight=_ext.FontWeight.Normal)->IGPUFont:
        """Initialize from font properties

        Args:
            family (str): font family, eg: Arial
            style (FontStyle, optional): font style. Defaults to FontStyle.Normal.
            weight (FontWeight, optional): font weight. Defaults to FontWeight.Normal.

        Returns:
            IGPUFont
        """
        config = cls()
        config._updating = True
        try:
            # TODO: Determine from path, do we even use these?
            config.family = family
            config.weight = weight
            config.style = style
        finally:
            config._updating = False
        config._resolve_props()
        return config
    
    def _resolve_props(self):
        """ family, weight or style has changed"""
        if self._updating:
            return  # prevent recursion
        self._updating = True
        try:
            props = _ext.font_manager.FontProperties(family=self.family, style=self.style.value, weight=self.weight.value)
            # Throws ValueError if not found
            self.path = _ext.font_manager.findfont(props, fallback_to_default=False)
        finally:
            self._updating = False
        self._load_path()
    
    @_ext.abc.abstractmethod
    def _load_path(self):
        """ Load the font """
        pass
    
    family = _ext.typed_property(str, default="", notify=_resolve_props)
    weight = _ext.typed_property(_ext.FontWeight, default=_ext.FontWeight.Normal, notify=_resolve_props)
    style = _ext.typed_property(_ext.FontStyle, default=_ext.FontStyle.Normal, notify=_resolve_props)
    align = _ext.typed_property(_ext.Align, default=_ext.Align.Default)
    path = _ext.typed_property(_ext.Path, default=None, notify=_load_path)
    
    color = _ext.typed_property(_ext.types.Color, default=_ext.parse_color("#FFFFFF"), converter=_ext.parse_color)
    shadow_color = _ext.typed_property(_ext.types.Color, default=_ext.parse_color("#FFFFFF"), converter=_ext.parse_color)
    shadow_offset = _ext.typed_property(_ext.types.Vector2f, default=[0.0, 0.0], converter=_ext.types.as_vector2f)
    shadow_blur = _ext.typed_property(int, default=0, converter=lambda x: x if x in [0,3,5] else 0)
    point_size = _ext.typed_property(int, default=12)
    angle = _ext.typed_property(float, default=0.0)
    
    @_ext.abc.abstractmethod
    def draw(self, viewport:_ext.IViewport, text:str, position:_ext.types.Vector2f, point_size:int=None,
             angle:float=None, color:_ext.types.Vector2f=None)->_ext.Rect:
        """ Draw the font with optional overrides
        
        Args:
            viewport(IViewport): viewport to draw to
            text(str): text to draw
            position(Vector): 2d position to draw text
            point_size(int): optional point_size, defaults to self.point_size
            angle(float): optional angle, defaults to self.angle
            color(Vector): optional color, defaults to self.color
        
        Returns:
            Bounds of text just drawn
        """
        pass
    
    @_ext.abc.abstractmethod
    def bounds(self, viewport:_ext.IViewport, text:str,
               position:_ext.types.Vector2f, point_size:int=None,
               angle:float=None)->_ext.Rect:
        """ Get the bounding box of this text without drawing it
        
        Args:
            viewport(IViewport): viewport to draw to
            text(str): text to draw
            position(Vector): 2d position to draw text
            point_size(int): optional point_size, defaults to self.point_size
            angle(float): optional angle, defaults to self.angle
        
        Returns:
            Bounds
        """
        pass