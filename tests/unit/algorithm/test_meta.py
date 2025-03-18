import pytest
from met_viewport_utils.algorithm import meta

def test_typed_property_basic():
    """Test basic typed property functionality"""
    class TestClass:
        value = meta.typed_property(int, 0)

    obj = TestClass()
    assert obj.value == 0  # Test default value
    obj.value = 42
    assert obj.value == 42  # Test setting value
    
def test_typed_property_type_checking():
    """Test type checking and conversion"""
    class TestClass:
        value = meta.typed_property(int, 0)
        
    obj = TestClass()
    obj.value = "42"  # Should convert string to int
    assert obj.value == 42
    assert isinstance(obj.value, int)

def test_typed_property_custom_converter():
    """Test custom converter function"""
    def custom_converter(value):
        # Convert any input to an integer and multiply by 2
        return int(value) * 2
    
    class TestClass:
        value = meta.typed_property(int, 0, converter=custom_converter)
    
    obj = TestClass()
    obj.value = 21.0  # Should be doubled by converter because it is a float
    assert obj.value == 42
    obj.value = "5"  # String should be converted to int and doubled
    assert obj.value == 10
    obj.value = 10  # Should not be doubled because it is correct type
    assert obj.value == 10

def test_typed_property_readonly():
    """Test readonly property"""
    class TestClass:
        value = meta.typed_property(int, 42, readonly=True)
    
    obj = TestClass()
    assert obj.value == 42
    with pytest.raises(AttributeError):
        obj.value = 10

def test_typed_property_notification():
    """Test property change notification"""
    notifications = []
    
    def on_change(instance):
        notifications.append(instance.value)
    
    class TestClass:
        value = meta.typed_property(int, 0, notify=on_change)
    
    obj = TestClass()
    obj.value = 42
    assert notifications == [42]

def test_alias_property_basic():
    """Test basic property aliasing using self reference"""
    class TestClass:
        _value = 0
        
        @property
        def base_value(self):
            return self._value
            
        @base_value.setter
        def base_value(self, val):
            self._value = val
            
        aliased = meta.alias_property(prop="self", path="base_value")
    
    obj = TestClass()
    obj.aliased = 42
    assert obj.aliased == 42
    assert obj.base_value == 42

def test_alias_property_readonly():
    """Test readonly alias property"""
    class TestClass:
        _value = 42
        
        @property
        def base_value(self):
            return self._value
            
        aliased = meta.alias_property(prop="self", path="base_value", readonly=True)
    
    obj = TestClass()
    assert obj.aliased == 42
    with pytest.raises(AttributeError):
        obj.aliased = 10

def test_alias_property_sequence():
    """Test alias property with sequence indexing"""
    class TestClass:
        def __init__(self):
            self.items = ["zero", "one", "two"]
        
        second_item = meta.alias_property(prop="self", path="items", index=1)
    
    obj = TestClass()
    assert obj.second_item == "one"
    obj.second_item = "updated"
    assert obj.second_item == "updated"
    assert obj.items[1] == "updated"
