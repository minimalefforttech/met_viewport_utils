# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    from .hud_item import HudItem
    from met_viewport_utils.interfaces import IGPUFont, IViewport
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.algorithm.meta import typed_property
    from met_viewport_utils.algorithm import types


class FontItem(_ext.HudItem):
    """Font HUD Item
    
    Args:
        text(str)
        font(IGPUFont) font implementation
    
    Properties:
        text(str)
        font(IGPUFont)
        data(dict) values to be referenced when drawing text
    """
    def __init__(self, text:str, font:_ext.IGPUFont):
        super().__init__()
        self.text = text
        self.font = font.copy()
        self.data = {}  # passed to text.format
    
    text = _ext.typed_property(str, "")
    
    def global_rect(self)->_ext.Rect:
        return _ext.Rect(
            _ext.types.as_vector2f(self.global_position()),
            self.size,
            self.font.align)
    
    def draw(self, viewport:_ext.IViewport):
        text = self.text.format(**self.data)
        screen_position = self.screen_position(viewport)
        
        rect = self.font.draw(text, screen_position)
        self.size = rect.size
