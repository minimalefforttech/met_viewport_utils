# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    import uuid
    import copy
    import re
    
_ALIAS_ATTR_PATH_REGEX = _ext.re.compile(r"((?:[_a-zA-Z][_a-zA-Z0-9]*(?:\(\)|\.|$))+)")
_ALIAS_ATTR_SETTER_REGEX = _ext.re.compile(r"^([_a-zA-Z][_a-zA-Z0-9]*)(\([a-zA-Z]+\))?$")

def typed_property(
    typ,
    default,
    converter=None,
    notify=None,
    property_id=None,
    readonly=False
):
    """Wrapper to create a typed property that preserves type on property set

    Args:
        typ (type): Property type
        default (Any): Default value to set
        converter (Callable, optional): Function used to set value, defaults to typ, set to False to disable
        notify(Callable, optional): Function to call when this value changes
        property_id(str, optional): Optionally specify the data key, defaults to a uuid
            This should not be the same name as the property or it will create a loop
        readonly(bool, optional): If True will not create a setter
    
    Returns:
        property
    """
    property_key = property_id or f"__{str(_ext.uuid.uuid4()).replace('-', '')}"
    if converter is None:
        converter = typ

    @property
    def _typed_property(self):
        if not hasattr(self, property_key):
            value = _ext.copy.copy(default) if default is not None else default
            setattr(self, property_key, value)
            return value
        return getattr(self, property_key)
    
    if not readonly:
        @_typed_property.setter
        def _typed_property(self, value):
            try:
                instance_check = isinstance(value, typ)
            except TypeError:
                # subscripted type, assume always convert
                instance_check = False
            if not instance_check:
                if not converter:
                    raise TypeError(f"Property expected a {typ}, got {type(value)}")
                value = converter(value)
            else:
                value = _ext.copy.copy(value)
            
            setattr(self, property_key, value)
            if notify:
                notify(self)
    
    return _typed_property

def alias_property(
    prop,
    path="",
    set_path=None,
    readonly=False,
    index=None
):
    """Aliases an existing property, this is to reduce boilerplate code and is not performant.

    Args:
        prop(property): property to reference
        path(str): path to the property on the property, this can have dots and callables
            eg: "vector.x()" or "component.ref().value"
        set_path(str): path to the setter on the property, this can have dots and callables
            if a function is specified, it takes one parameter, it doesn't matter what the param name is
            if a variable is specified, it will assign (ref.to.prop = value)
            eg: "vector.setX(x)" or "component.ref().value"
        readonly(bool, optional): If True will not create a setter
        index(int, optional): If set will add an index to the end of both getter and setters
    
    Returns:
        property
    """
    if not path and index is None:
        raise ValueError("path and/or index must be specified")
    set_path = set_path or path
    if path and not _ALIAS_ATTR_PATH_REGEX.match(path):
        raise ValueError("path is invalid, must be only attrs or callables without params, eg: attr.subattr().x")
    
    setter_prop = None
    setter_arg = None
    if not readonly and set_path:
        if "." in set_path:
            set_path, setter = set_path.rsplit(".", 1)
            if not _ALIAS_ATTR_PATH_REGEX.match():
                raise ValueError("set_path is invalid, must be only attrs or callables without params, last part takes one param if callable, eg: attr.subattr().set_x(v)")
        else:
            setter = set_path
            set_path = ""
    
        if match := _ALIAS_ATTR_SETTER_REGEX.match(setter):
            setter_prop, setter_arg = match.groups()
        else:
            raise ValueError("set_path is invalid, last part takes one param if callable or must be attr")
    if prop == "self":
        accessor = lambda self: self
    elif isinstance(prop, property):
        accessor = lambda self: prop.fget(self)
    else:
        raise ValueError("prop must be 'self' or property accessor")
    
    @property
    def _alias_property(self):
        value = accessor(self)

        for each in path.split("."):
            if not each:
                continue
            value = getattr(value, each.split("(")[0])
            if "()" in each:
                value = value()
        if index is not None:
            return value[index]
        return value
    
    if not readonly:
        @_alias_property.setter
        def _alias_property(self, value):
            obj = accessor(self)
            for each in set_path.split("."):
                if not each:
                    continue
                obj = getattr(obj, each.split("(")[0])
                if "()" in each:
                    obj = obj()
            if setter_arg:
                obj = getattr(obj, setter_prop)
                if index is not None:
                    obj = obj[index]
                obj(value)
            elif setter_prop:
                if index:
                    obj = getattr(obj, setter_prop)
                    obj[index] = value
                else:
                    setattr(obj, setter_prop, value)
            elif index is not None:
                obj[index] = value
    
    return _alias_property
