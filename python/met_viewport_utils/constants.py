# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
"""Generic constants
"""
import enum as _enum

class Axis(_enum.IntFlag):
    """ XYZ axis flags
    """
    Invalid = 0
    X = _enum.auto()
    Y = _enum.auto()
    Z = _enum.auto()
    XY = X|Y
    XZ = X|Z
    YZ = Y|Z
    XYZ = X|Y|Z

    
class GPUShaderState(_enum.IntFlag):
    """GPU state flag for drawing
    """
    Default = _enum.auto()
    UseAlpha = _enum.auto()
    UseDepth = _enum.auto()

class GPUShaderPrimitiveType(_enum.Enum):
    """Convenience class for primitive drawing types
    """
    Points = "POINTS"
    Lines = "LINES"
    Tris = "TRIS"
    LineStrip = "LINE_STRIP"
    LineLoop = "LINE_LOOP"
    TriStrip = "TRI_STRIP"
    TriFan = "TRI_FAN"
    LinesAdj = "LINES_ADJ"
    TrisAdj = "TRIS_ADJ"
    LineStripAdj = "LINE_STRIP_ADJ"


class GPUShaderUniformType(_enum.Enum):
    """Shader uniform type enum
    """
    Block = _enum.auto()
    Bool = _enum.auto()
    Float = _enum.auto()
    Int = _enum.auto()
    Sampler = _enum.auto()
    VectorFloat = _enum.auto()
    VectorInt = _enum.auto()
    

class FontStyle(_enum.Enum):
    """matplotlib font style"""
    Normal = "normal"
    Oblique = "oblique"
    Italic = "italic"
    Unknown = "unknown"


class FontWeight(_enum.Enum):
    """matplotlib font weight"""
    UltraLight = "ultralight"
    Light = "light"
    Normal = "normal"
    Regular = "regular"
    Semibold = "semibold"
    Bold = "bold"
    Heavy = "heavy"
    ExtraBold = "extra bold"
    Black = "black"
    Unknown = "unknown"

class Align(_enum.Flag):
    """2D Alignment flags"""
    Left = _enum.auto()
    Right = _enum.auto()
    Top = _enum.auto()
    HCenter = _enum.auto()
    VCenter = _enum.auto()
    Bottom = _enum.auto()

    Center = HCenter|VCenter
    TopLeft = Top|Left
    TopRight = Top|Right
    BottomLeft = Bottom|Left
    BottomRight = Bottom|Right
    LeftCenter = Left|VCenter
    RightCenter = Right|VCenter
    TopCenter = Top|HCenter
    BottomCenter = Bottom|HCenter

    Default = Left|Bottom

class MouseButton(_enum.Enum):
    """Standard mouse buttons """
    NoButton = 0
    Left = _enum.auto()
    Middle = _enum.auto()
    Right = _enum.auto()
    
class KeyboardModifier(_enum.IntFlag):
    """Keyboard Modifier"""
    NoKeyboardModifier = 0
    Shift = _enum.auto()
    Ctrl = _enum.auto()
    Alt = _enum.auto()


class InteractionFlags(_enum.IntFlag):
    """Item valid interactions"""
    NoInteraction = 0
    Selectable = _enum.auto()
    Draggable = _enum.auto()
    # TODO: Drop events, inputs


class ItemState(_enum.IntFlag):
    """Item Active interactions"""
    NoState = 0
    Enabled = _enum.auto()
    Visible = _enum.auto()
    Selected = _enum.auto()
    Dragging = _enum.auto()
    Hovered = _enum.auto()
