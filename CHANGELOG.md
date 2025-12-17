# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of whyfail library
- Context manager API: `with whyfail.explain():`
- Decorator API: `@whyfail.explain_errors()`
- Human-readable explanations for 9 common exception types:
  - KeyError
  - IndexError
  - TypeError
  - ValueError
  - AttributeError
  - NameError
  - ZeroDivisionError
  - FileNotFoundError
  - ImportError
- Pluggable explainer system: `register_explainer()`
- Configuration API: `whyfail.configure()`
- Utility functions for error context analysis
- Comprehensive test suite
- Example scripts demonstrating all features
