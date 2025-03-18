# Contributing to met_viewport_utils

This document provides guidelines for contributing to the met_viewport_utils package, a template interface library for viewport management in DCC applications.

## Development Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Code Structure

- `python/met_viewport_utils/` - Main package source
  - `algorithm/` - Mathematical and utility functions
  - `interfaces/` - Abstract base classes for DCC implementations
  - `items/` - Viewport item implementations
  - `shape/` - Geometric primitives and operations

## Testing

We use pytest for testing:

1. Tests are located in `tests/unit/`
2. Follow the module structure for test organization
3. Run tests with:
   ```bash
   pytest
   ```
4. Maintain 80% code coverage across project
5. Maintain 70% code coverage per file
6. Write tests that serve as implementation examples
7. Do not include any DCC specific functionality in this repository

## Documentation

1. Document new interfaces thoroughly:
   - Purpose and usage
   - Implementation requirements
   - Expected behavior

2. Update API documentation when adding/modifying features:
   - Keep module descriptions current
   - Document class responsibilities
   - Explain non-obvious implementations

3. Include docstrings:
   ```python
   def function_name(param: type) -> return_type:
       """Short description.

       Longer description if needed.

       Args:
           param: Parameter description

       Returns:
           Description of return value
       """
   ```

## Code Style

1. Follow PEP 8 guidelines
2. Use type hints
3. Keep functions focused and modular
4. Write clear, descriptive variable names
5. Comment complex algorithms
6. Separate interface and implementation concerns

## Pull Request Process

1. Create a feature branch
2. Write tests for new functionality
3. Update documentation
4. Run full test suite
5. Submit PR with clear description:
   - Purpose of changes
   - Implementation approach
   - Testing strategy
   - Documentation updates

## DCC-Specific Implementations

When implementing DCC-specific functionality:

1. Inherit from appropriate interface classes
2. Follow interface contracts strictly
3. Document DCC-specific considerations
4. Provide usage examples
5. Test thoroughly with mocked DCC environment

## Questions and Support

For questions or assistance:
1. Check existing documentation
2. Review test examples
3. Open an issue for clarification

## Release Process

1. Update version in setup.py
2. Update changelog
3. Run full test suite
4. Create release notes
5. Tag release in git
