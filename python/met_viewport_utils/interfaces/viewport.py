# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    import abc
    import typing
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.algorithm import types


class IViewport(_ext.abc.ABC):
    """Viewport interface, re-implement in the required DCC
    """
    def rect(self)->_ext.Rect:
        pass
    
    @_ext.abc.abstractmethod
    def screen_to_world(self, screen_position:_ext.types.Vector2fCompat, depth_point:_ext.types.Vector3f)->_ext.types.Vector3f:
        """From a position in the screen, return a tuple representing the ray origin and direction

        Args:
            screen_position (Vector2f): screen position
            depth_point(Vector3f): position in space to match

        Returns:
            Vector3f position
        """
        pass
    
    @_ext.abc.abstractmethod
    def screen_to_ray(self, screen_position:_ext.types.Vector2fCompat)->_ext.typing.Tuple[_ext.types.Vector3f]:
        """From a position in the screen, return a tuple representing the ray origin and direction

        Args:
            screen_position (Vector2f): screen position

        Returns:
            Vector3f origin, ray_dir
        """
        pass
    
    def world_to_screen(self, world_position:_ext.types.Vector3fCompat)->_ext.types.Vector2f:
        """From a position in the screen, return a tuple representing the ray origin and direction

        Args:
            world_position (Vector2f): screen position

        Returns:
            Vector2d screen_position
        """
        pass
