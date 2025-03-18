# 1. Testing Strategy

## Status
Completed

## Stakeholders
Alex Telford (Engineer)

## Context
The met_viewport_utils package provides template interfaces and utilities for viewport management in Digital Content Creation (DCC) software. As a template package, it needs:
1. Clear documentation of the interfaces for DCC-specific implementations
2. Basic testing infrastructure for the template components
3. Example implementations to guide DCC-specific adaptations

## Decision
We will implement the following testing strategy:

### Testing Strategy
- Use pytest as the primary testing framework
- Create test files matching the module structure in a `tests/` directory
- Focus on testing template interfaces and base implementations
- Mock DCC-specific functionality where needed to keep this tests light
- Ensure tests serve as implementation examples
- Aim for 80% code coverage

## Consequences

### Positive
1. Clear interface specifications for DCC implementations
2. Tests serve dual purpose as implementation examples

### Negative
1. Initial effort to create template test suite
2. Limited testing of DCC-specific functionality may not catch issues

### Mitigations
1. Use existing blender usage as reference for test patterns
2. Keep example implementations simple and focused
3. Clear separation between template and DCC-specific concerns
