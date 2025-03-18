# met_viewport_utils

A Python library providing a flexible, DCC-agnostic framework for viewport interaction in 3D applications like Maya, Blender, and Houdini.

## Features

- **DCC-Independent Core**: MIT-licensed core library that works across different 3D applications
- **Viewport Interaction**: Lightweight api for handling mouse events and viewport manipulation
- **Shape Generation**: Built-in utilities for creating and manipulating 2D shapes
- **HUD Elements**: Support for heads-up display elements including text and interactive widgets

## Installation

```bash
pip install met-viewport-utils
```

## Quick Start

```python
from met_viewport_utils.items.point_item import PointItem
from met_viewport_utils.constants import InteractionFlags

# Create an interactive point
point = PointItem()
point.position = [100, 100, 0]
point.flags = InteractionFlags.Selectable | InteractionFlags.Draggable

# Create a child item that inherits transformations
child = PointItem()
child.parent = point
child.position = [50, 0, 0]  # Relative to parent
```

## Documentation

- [API Reference](docs/api.md): Detailed documentation of all modules and classes
- [Examples](docs/examples.md): Code examples and usage patterns
- [Contributing](docs/CONTRIBUTING.md): Guidelines for development and contributions
- [Changelog](docs/CHANGELOG.md): Version history and updates

## DCC Implementation

The library is designed to be implemented by DCC-specific adapters. Available implementations:

- [met_blender_viewport_utils](https://github.com/your-username/met_blender_viewport_utils): Blender implementation
- Maya implementation (coming soon)
- Houdini implementation (coming soon)

## Architecture Decisions

Key architectural decisions are documented in the Architecture Decision Records (ADRs):

- [ADR-001](docs/architecture-decision-records/001-code-separation.md): Code Separation Strategy
- [ADR-002](docs/architecture-decision-records/002-testing.md): Testing Framework
- [ADR-003](docs/architecture-decision-records/003-docmentation.md): Documentation Strategy

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Development Status

Current version: 0.1.4

This library is under active development. Major features are stable, but APIs may evolve as new DCC implementations are added.
