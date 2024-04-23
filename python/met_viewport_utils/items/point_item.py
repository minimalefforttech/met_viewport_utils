# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    import copy
    import numpy
    from met_viewport_utils.constants import (
        MouseButton,
        KeyboardModifier,
        InteractionFlags,
        ItemState,
        Align)
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.interfaces import IHierarchyItem, IViewport
    from met_viewport_utils.algorithm.meta import typed_property
    from met_viewport_utils.algorithm import types


class PointItem(_ext.IHierarchyItem):
    """3D Point item"""
    def __init__(self):
        super().__init__()
        self.__drag_start:_ext.types.Vector2f = _ext.types.as_vector2f([0, 0])
        self.__drag_data = None
        
    flags:_ext.InteractionFlags = _ext.typed_property(_ext.InteractionFlags, default=_ext.InteractionFlags.NoInteraction)
    state:_ext.ItemState = _ext.typed_property(_ext.ItemState, default=_ext.ItemState.Enabled|_ext.ItemState.Visible)
    is2d:bool = _ext.typed_property(bool, default=False)
    
    # TODO: Store as a transform matrix
    position:_ext.types.Vector3f = _ext.typed_property(_ext.types.Vector3f, default=[0, 0, 0], converter=_ext.types.as_vector3f)
    
    # Note this position may not be up to date depending on parent enabled state
    _local_mouse_position:_ext.types.Vector2f = _ext.typed_property(_ext.types.Vector2f, default=[0, 0], converter=_ext.types.as_vector2f)
    

    def global_position(self)->_ext.types.Vector3f:
        # Map relative to root
        try:
            parent:PointItem = next(self.iter_parents(PointItem))
        except StopIteration:
            return _ext.copy.copy(self.position)
        
        if self.is2d != parent.is2d:
            # Cannot parent a 2d item to 3d or vice versa, stop here to prevent overflow
            return _ext.copy.copy(self.position)
        return parent.global_position() + self.position
    
    def screen_position(self, viewport:_ext.IViewport)->_ext.types.Vector2f:
        if self.is2d:
            return _ext.types.as_vector2f(self.global_position())
        return viewport.world_to_screen(self.global_position())
    
    def mouse_pressed(self,
                      viewport:_ext.IViewport,
                      local_position:_ext.types.Vector2f,
                      screen_position:_ext.types.Vector2f,
                      button:_ext.MouseButton,
                      modifier:_ext.KeyboardModifier)->bool:
        if not self.state & _ext.ItemState.Enabled:
            return False
        local_position = _ext.types.as_vector2f(local_position)
        screen_position = _ext.types.as_vector2f(screen_position)
        accepted = False
        for child in self.iter_descendants(PointItem):
            if isinstance(child, PointItem):
                if child.mouse_pressed(
                    viewport,
                    local_position-self.screen_position(viewport),
                    screen_position,
                    button,
                    modifier
                ):
                    accepted = True
        if not (self.state & _ext.ItemState.Hovered):
            return accepted
        
        if self.flags & _ext.InteractionFlags.Selectable:
            self._update_selection(modifier)
            accepted = True
            
        if self.flags & _ext.InteractionFlags.Draggable:
            # TODO: Only set this flag once press and move
            self.state |= _ext.ItemState.Dragging
            self.__drag_start = _ext.types.as_vector2f(local_position)
            self.__drag_data = self._get_drag_data()
            accepted = True
        return accepted
    
    def mouse_released(self,
                       viewport:_ext.IViewport,
                       local_position:_ext.types.Vector2f,
                       screen_position:_ext.types.Vector2f,
                       button:_ext.MouseButton,
                       modifier:_ext.KeyboardModifier)->bool:
        self.state &= ~_ext.ItemState.Dragging
        if not (self.state & _ext.ItemState.Enabled):
            return False
        local_position = _ext.types.as_vector2f(local_position)
        screen_position = _ext.types.as_vector2f(screen_position)
        accepted = False
        for child in self.iter_descendants(PointItem):
            if child.mouse_released(
                viewport,
                local_position-self.screen_position(viewport),
                screen_position,
                button,
                modifier
            ):
                accepted = True
        return accepted
    
    def mouse_moved(self,
                    viewport:_ext.IViewport,
                    local_position:_ext.types.Vector2f,
                    screen_position:_ext.types.Vector2f,
                    modifier:_ext.KeyboardModifier):
        if not (self.state & _ext.ItemState.Enabled):
            return
        local_position = _ext.types.as_vector2f(local_position)
        screen_position = _ext.types.as_vector2f(screen_position)
        # TODO: Optimize this, not every item has mouse interaction
        # Also some children need to track the mouse, should support this
        self._local_mouse_position = local_position
        if self._is_under_mouse(viewport, local_position, screen_position):
            self.state |= _ext.ItemState.Hovered
        else:
            self.state &= ~_ext.ItemState.Hovered

        for child in self.iter_descendants(PointItem):
            child.mouse_moved(
                viewport,
                local_position-self.screen_position(viewport),
                screen_position,
                modifier
            )
        
        if not self.state & (_ext.ItemState.Hovered|_ext.ItemState.Dragging):
            return
    
        if (self.flags & _ext.InteractionFlags.Draggable) and (self.state & _ext.ItemState.Dragging):
            delta = self._local_mouse_position - self.__drag_start
            self._drag_move(viewport, self.__drag_data, delta, modifier)
        return
    
    def draw(self, viewport:_ext.IViewport):
        return

    def _get_drag_data(self):
        """Override this to choose the stored origin data when dragging, defaults to self.position"""
        return self.position

    def _drag_move(self,
                   viewport:_ext.IViewport,
                   start_data,
                   delta:_ext.types.Vector2f,
                   modifier:_ext.KeyboardModifier):
        """Override this to change how the drag behaviour behaves"""
        self.position = _ext.types.as_vector3f(start_data) + _ext.types.as_vector3f(delta)
        # TODO: move other selected items
        

    def _update_selection(self, modifier:_ext.KeyboardModifier):
        """ Triggers selection update """
        root = self.get_root()
        if not modifier & _ext.KeyboardModifier.Shift:
            if isinstance(root, PointItem) and (root.state & _ext.InteractionFlags.Selectable):
                root.state &= ~_ext.ItemState.Selected
            
            for item in root.iter_descendants(PointItem):
                item.state &= ~_ext.ItemState.Selected
        
        if modifier & _ext.KeyboardModifier.Ctrl:
            item.state ^= _ext.ItemState.Selected
        else:
            item.state |= _ext.ItemState.Selected
    
    def screen_rect(self, viewport:_ext.IViewport)->_ext.Rect:
        # TODO: Expose point size for mouse interaction
        return _ext.Rect(self.screen_position(viewport), _ext.types.as_vector2f((20, 20)), _ext.Align.Center)
        
    def _is_under_mouse(self, viewport:_ext.IViewport, local_position:_ext.types.Vector2f, screen_position:_ext.types.Vector2f)->bool:
        """Is this position on top of this item? Overload for custom shapes"""
        return self.screen_rect(viewport).contains(screen_position)
