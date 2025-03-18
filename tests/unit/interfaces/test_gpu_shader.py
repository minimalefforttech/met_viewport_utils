import pytest
from unittest.mock import Mock
from met_viewport_utils.interfaces.gpu_shader import IGPUShader
from met_viewport_utils.constants import GPUShaderPrimitiveType, GPUShaderState, GPUShaderUniformType

class MockShader:
    """Mock for internal shader object"""
    def __init__(self):
        self.uniform_float = Mock()
        self.uniform_int = Mock()
        self.uniform_bool = Mock()
        self.uniform_sampler = Mock()

class MockGPUShader(IGPUShader):
    """Concrete implementation for testing"""
    def __init__(self, shader=None):
        super().__init__(shader or MockShader())
        self._last_batch = True  # Enable uniform setting
        
    def draw(self, viewport, vertex_in, primitive_type=None, indices=None, size=None, state=None, **kwargs):
        """Mock draw implementation"""
        self._prep_shader()
        # Store draw parameters for testing
        self.last_draw = {
            'viewport': viewport,
            'vertex_in': vertex_in,
            'primitive_type': primitive_type or self.primitive_type,
            'indices': indices,
            'size': size or self.size,
            'state': state or self.state,
            'kwargs': kwargs
        }

def test_shader_init():
    """Test basic shader initialization"""
    shader = MockGPUShader()
    assert shader.primitive_type == GPUShaderPrimitiveType.Points
    assert shader.state == GPUShaderState.Default
    assert shader.size == 0.0

def test_shader_properties():
    """Test shader property setters"""
    shader = MockGPUShader()
    
    shader.primitive_type = GPUShaderPrimitiveType.Lines
    assert shader.primitive_type == GPUShaderPrimitiveType.Lines
    
    shader.state = GPUShaderState.UseAlpha
    assert shader.state == GPUShaderState.UseAlpha
    
    shader.size = 2.0
    assert shader.size == 2.0

def test_shader_uniform_float():
    """Test float uniform handling"""
    shader = MockGPUShader()
    shader.set_uniform("scale", [1.5])  # Use list for float values
    
    # Should infer float type from list content
    assert shader._uniform_types["scale"] == GPUShaderUniformType.Float
    shader.shader.uniform_float.assert_called_with("scale", [1.5])

def test_shader_uniform_int():
    """Test integer uniform handling"""
    shader = MockGPUShader()
    shader.set_uniform("count", [1, 2, 3])
    
    # Should infer int type from list content
    assert shader._uniform_types["count"] == GPUShaderUniformType.Int
    shader.shader.uniform_int.assert_called_with("count", [1, 2, 3])

def test_shader_uniform_bool():
    """Test boolean uniform handling"""
    shader = MockGPUShader()
    shader.set_uniform("enabled", True)
    
    assert shader._uniform_types["enabled"] == GPUShaderUniformType.Bool
    shader.shader.uniform_bool.assert_called_with("enabled", True)

def test_shader_defaults():
    """Test default uniform values"""
    shader = MockGPUShader()
    shader._last_batch = False  # Disable uniform setting to store defaults
    
    # Set some defaults
    shader.set_uniform("scale", [1.0])  # Use list for float values
    shader.set_uniform("enabled", True)
    
    assert shader.defaults == {"scale": [1.0], "enabled": True}
    
    # Enable uniform setting and draw
    shader._last_batch = True
    mock_viewport = Mock()
    shader.draw(mock_viewport, {"position": [0, 0]})
    
    # Should have set defaults during _prep_shader
    shader.shader.uniform_float.assert_called_with("scale", [1.0])
    shader.shader.uniform_bool.assert_called_with("enabled", True)

def test_shader_uniform_sampler():
    """Test sampler uniform handling when type is known"""
    shader = MockGPUShader()
    shader._uniform_types["tex"] = GPUShaderUniformType.Sampler
    texture = Mock()
    shader.set_uniform("tex", texture)
    
    shader.shader.uniform_sampler.assert_called_with("tex", texture)

def test_shader_uniform_known_type():
    """Test setting uniform with pre-known type"""
    shader = MockGPUShader()
    shader._uniform_types["value"] = GPUShaderUniformType.Float
    shader.set_uniform("value", [1.5])
    
    shader.shader.uniform_float.assert_called_with("value", [1.5])

def test_shader_uniform_vector_float_not_implemented():
    """Test VectorFloat uniform raises NotImplementedError"""
    shader = MockGPUShader()
    shader._uniform_types["vec"] = GPUShaderUniformType.VectorFloat
    
    with pytest.raises(NotImplementedError) as excinfo:
        shader.set_uniform("vec", [1.0, 2.0, 3.0])
    assert "VectorFloat type not yet implemented" in str(excinfo.value)

def test_shader_uniform_vector_int_not_implemented():
    """Test VectorInt uniform raises NotImplementedError"""
    shader = MockGPUShader()
    shader._uniform_types["vec"] = GPUShaderUniformType.VectorInt
    
    with pytest.raises(NotImplementedError) as excinfo:
        shader.set_uniform("vec", [1, 2, 3])
    assert "VectorInt type not yet implemented" in str(excinfo.value)

def test_shader_uniform_block_not_implemented():
    """Test Block uniform raises NotImplementedError"""
    shader = MockGPUShader()
    shader._uniform_types["block"] = GPUShaderUniformType.Block
    
    with pytest.raises(NotImplementedError) as excinfo:
        shader.set_uniform("block", {})
    assert "Block type not yet implemented" in str(excinfo.value)

def test_shader_uniform_invalid_type():
    """Test invalid uniform type raises ValueError"""
    shader = MockGPUShader()
    
    with pytest.raises(ValueError) as excinfo:
        shader.set_uniform("invalid", None)
    assert "Unrecognized value type" in str(excinfo.value)

def test_shader_draw_params():
    """Test draw parameter handling"""
    shader = MockGPUShader()
    mock_viewport = Mock()
    vertex_data = {"position": [0, 0]}
    
    shader.draw(
        mock_viewport,
        vertex_data,
        primitive_type=GPUShaderPrimitiveType.Lines,
        size=2.0,
        state=GPUShaderState.UseAlpha,
        custom_param=42
    )
    
    # Verify draw parameters were captured
    assert shader.last_draw["viewport"] == mock_viewport
    assert shader.last_draw["vertex_in"] == vertex_data
    assert shader.last_draw["primitive_type"] == GPUShaderPrimitiveType.Lines
    assert shader.last_draw["size"] == 2.0
    assert shader.last_draw["state"] == GPUShaderState.UseAlpha
    assert shader.last_draw["kwargs"]["custom_param"] == 42
