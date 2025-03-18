import pytest
from unittest.mock import Mock, call
from met_viewport_utils.interfaces.gpu_state import IGPURestoreState
from met_viewport_utils.constants import GPUShaderState

class MockGPUState(IGPURestoreState):
    """Concrete implementation for testing"""
    def __init__(self, flags):
        super().__init__(flags)
        self._current_states = {
            GPUShaderState.UseAlpha: "NONE",
            GPUShaderState.UseDepth: ("NONE", False)
        }
    
    @classmethod
    def _get_state(cls, state):
        if state == GPUShaderState.UseAlpha:
            return cls._current_states[state]
        elif state == GPUShaderState.UseDepth:
            return cls._current_states[state]
    
    @classmethod
    def _set_state(cls, state, param):
        cls._current_states[state] = param

def test_gpu_state_alpha():
    """Test alpha state handling"""
    # Set initial state
    MockGPUState._current_states = {
        GPUShaderState.UseAlpha: "NONE",
        GPUShaderState.UseDepth: ("NONE", False)
    }
    
    with MockGPUState(GPUShaderState.UseAlpha) as state:
        # Should set alpha blend mode to ALPHA
        assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "ALPHA"
    
    # Should restore original state
    assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "NONE"

def test_gpu_state_depth():
    """Test depth state handling"""
    # Set initial state
    MockGPUState._current_states = {
        GPUShaderState.UseAlpha: "NONE",
        GPUShaderState.UseDepth: ("NONE", False)
    }
    
    with MockGPUState(GPUShaderState.UseDepth) as state:
        # Should set depth test mode to LESS_EQUAL with True
        assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("LESS_EQUAL", True)
    
    # Should restore original state
    assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("NONE", False)

def test_gpu_state_multiple():
    """Test handling multiple states"""
    # Set initial state
    MockGPUState._current_states = {
        GPUShaderState.UseAlpha: "NONE",
        GPUShaderState.UseDepth: ("NONE", False)
    }
    
    with MockGPUState(GPUShaderState.UseAlpha | GPUShaderState.UseDepth) as state:
        # Both states should be set
        assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "ALPHA"
        assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("LESS_EQUAL", True)
    
    # Both states should be restored
    assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "NONE"
    assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("NONE", False)

def test_gpu_state_exception():
    """Test state restoration when exception occurs"""
    # Set initial state
    MockGPUState._current_states = {
        GPUShaderState.UseAlpha: "NONE",
        GPUShaderState.UseDepth: ("NONE", False)
    }
    
    try:
        with MockGPUState(GPUShaderState.UseAlpha) as state:
            raise ValueError("Test exception")
    except ValueError:
        pass
    
    # State should still be restored despite exception
    assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "NONE"

def test_gpu_state_nested():
    """Test nested state managers"""
    # Set initial state
    MockGPUState._current_states = {
        GPUShaderState.UseAlpha: "NONE",
        GPUShaderState.UseDepth: ("NONE", False)
    }
    
    with MockGPUState(GPUShaderState.UseAlpha) as state1:
        assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "ALPHA"
        
        with MockGPUState(GPUShaderState.UseDepth) as state2:
            # Both states should be active
            assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "ALPHA"
            assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("LESS_EQUAL", True)
        
        # Depth should be restored, alpha should still be active
        assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "ALPHA"
        assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("NONE", False)
    
    # Both states should be restored
    assert MockGPUState._current_states[GPUShaderState.UseAlpha] == "NONE"
    assert MockGPUState._current_states[GPUShaderState.UseDepth] == ("NONE", False)
