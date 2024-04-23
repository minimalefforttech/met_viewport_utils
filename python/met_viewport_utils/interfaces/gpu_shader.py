# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    import abc
    import typing
    from met_viewport_utils.constants import (
        GPUShaderPrimitiveType,
        GPUShaderUniformType,
        GPUShaderState)
    from met_viewport_utils.algorithm.meta import typed_property
    from .viewport import IViewport


class IGPUShader(_ext.abc.ABC):
    """ Simple wrapper around a GPU shader draw
    
    Args:
        shader(GPUShader): Shader to draw
    
    Properties:
        shader(GPUShader): Internal shader
        primitive(_ext.GPUShaderPrimitiveType): primitive drawing type
        state(GPUShaderState): Optional state to set while drawing this shader
        size(float): Width of points or lines
    """
    shader = None  # Internal shader pointer
    primitive_type = _ext.typed_property(_ext.GPUShaderPrimitiveType, default=_ext.GPUShaderPrimitiveType.Points)
    state = _ext.typed_property(_ext.GPUShaderState, default=_ext.GPUShaderState.Default)
    size = _ext.typed_property(float, default=0.0)

    def __init__(self, shader):
        self.shader = shader
        self._uniform_types = {}
        self.defaults = {}
    
    def set_uniform(self, name:str, value):
        """ Set a uniform value, if this is the first run, it becomes a default
        
        Args:
            name(str): name of shader uniform
            value(Any): value to set
        
        Raises:
            NotImplementedError: If type is not yet supported by met_blender_utils
        """
        if not self._last_batch:
            self.defaults[name] = value
            return
        type_ = self._uniform_types.get(name)
        if type_:
            match type_:
                case _ext.GPUShaderUniformType.Float:
                    self.shader.uniform_float(name, value)
                case _ext.GPUShaderUniformType.Int:
                    self.shader.uniform_int(name, value)
                case _ext.GPUShaderUniformType.Bool:
                    self.shader.uniform_bool(name, value)
                case _ext.GPUShaderUniformType.Sampler:
                    self.shader.uniform_sampler(name, value)
                case _ext.GPUShaderUniformType.VectorFloat:
                    # TODO
                    raise NotImplementedError("VectorFloat type not yet implemented, set via .shader.uniform_vector_float")
                    # self.shader.uniform_vector_float(name, value)
                case _ext.GPUShaderUniformType.VectorInt:
                    raise NotImplementedError("VectorInt type not yet implemented, set via .shader.uniform_vector_int")
                    # self.shader.uniform_vector_int(name, value)
                case _ext.GPUShaderUniformType.Block:
                    raise NotImplementedError("Block type not yet implemented, set via .shader.uniform_block")
                    # self.shader.uniform_block(name, value)
            return
        # If not set, assume based on type
        self._set_uniform_by_type(name, value)
    
    def _prep_shader(self):
        """ Sets the default properties on the shader
        """
        for k, v in self.defaults.items():
            self.set_uniform(k, v)
        
    def _set_uniform_by_type(self, name:str, value):
        if isinstance(value, bool):
            self._uniform_types[name] = _ext.GPUShaderUniformType.Bool
            self.shader.uniform_bool(name, value)
        elif isinstance(value, (list, tuple)) and value:
            sub_value = value[0]
            if isinstance(sub_value, int):
                self._uniform_types[name] = _ext.GPUShaderUniformType.Int
                self.shader.uniform_int(name, value)
            else:
                self._uniform_types[name] = _ext.GPUShaderUniformType.Float
                self.shader.uniform_float(name, value)
        else:
            raise ValueError(f"Unrecognized value type, may not yet be implemented: {name}: {type(value)}")
    
    @_ext.abc.abstractmethod
    def draw(self,
             viewport:_ext.typing.Optional[_ext.IViewport],
             vertex_in:_ext.typing.Dict[str, _ext.typing.Any],
             primitive_type:_ext.GPUShaderPrimitiveType=None,
             indices:_ext.typing.Optional[_ext.typing.List[int]]=None,
             size:_ext.typing.Optional[float]=None,
             state:_ext.typing.Optional[_ext.GPUShaderState]=None,
             **kwargs):
        """Draw this shader

        Args:
            viewport(IViewport): viewport to render to
            vertex_in (Dict[str, Any]): Inputs to vertex shader
            primitive_type (GPUShaderPrimitiveType, optional): Primitive override
            indices (List[int], optional): indices map, optional
            size (float, optional): size override
            state (GPUShaderState, optional): state override
        """
        pass