# 001 - Code Separation for Viewport Utils

## Status

Completed

## Stakeholders
Alex Telford (Engineer)

## Context

The goal is to create a set of Python utilities for interacting with 3D viewports (like those in Blender, Houdini and Maya). A key requirement is to have a core API that is independent of any specific application's API. This separation is crucial for licensing: the core library should be MIT-licensed, while application-specific integrations (e.g., with Blender or Maya) can have different licenses. This avoids "GPL pollution" of the core library, allowing broader usage and contribution. The core API should be simple, well-structured, and serve as a solid base for building viewport interaction tools.

## Decision

Separate the code into a core library (`met_viewport_utils`) and application-specific adapters eg: `met_blender_viewport_utils`.

- The core library will contain all the fundamental logic for viewport interaction, including algorithms, data structures, and interfaces. It will be independent of any specific 3D application.
- Application-specific adapters will be created as separate projects/packages. These adapters will use the core library and provide the necessary glue code to integrate with the target application's API (e.g., Blender's `bpy` module, Maya's `maya.cmds` module).

