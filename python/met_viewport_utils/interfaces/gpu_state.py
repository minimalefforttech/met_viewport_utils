# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    from met_viewport_utils.constants import GPUShaderState
    import typing
    import abc


class IGPURestoreState(_ext.abc.ABC):
    """Context manager to temporarily set and restore state while drawing

    Args:
        flags (GpuShaderState): State flags to set
    
    Usage:
        with GpuRestoreState(GpuShaderState.Alpha|GpuShaderState.Depth):
            batch.draw()
    """
    def __init__(self, flags:_ext.GPUShaderState):
        self._flags:_ext.GPUShaderState = flags
        self._last_state:_ext.typing.Dict[str, int] = {}
    
    @classmethod
    @_ext.abc.abstractmethod
    def _get_state(cls, state:_ext.GPUShaderState):
        pass
    
    @classmethod
    @_ext.abc.abstractmethod
    def _set_state(cls, state:_ext.GPUShaderState, param):
        pass
    
    
    def __enter__(self):
        self._last_state = {}
        if _ext.GPUShaderState.UseAlpha in self._flags:
            self._last_state["blend"] = self._get_state(_ext.GPUShaderState.UseAlpha)
            self._set_state(_ext.GPUShaderState.UseAlpha, "ALPHA")
        if _ext.GPUShaderState.UseDepth in self._flags:
            # TODO: Should use actual flags here...
            self._last_state["depth"] = self._get_state(_ext.GPUShaderState.UseDepth)
            self._set_state(_ext.GPUShaderState.UseDepth, ("LESS_EQUAL", True))
    
    def __exit__(self, *_):
        if _ext.GPUShaderState.UseAlpha in self._flags:
            self._set_state(_ext.GPUShaderState.UseAlpha, self._last_state["blend"])
        if _ext.GPUShaderState.UseDepth in self._flags:
            self._set_state(_ext.GPUShaderState.UseDepth, self._last_state["depth"])
        self._last_state = {}
