# Windows Security Controls Generator

A modular Streamlit application for generating Windows security artifacts including Group Policy Objects (GPO), PowerShell scripts, registry files, and batch scripts.

## Overview

This application follows a modular architecture with clear separation of concerns:

- **Core**: Abstract interfaces and base classes
- **Controls**: Security control definitions and logic  
- **Generators**: Artifact generation engines
- **UI**: User interface renderers
- **Services**: Business logic services
- **Examples**: Usage examples and templates

## Quick Start

```bash
streamlit run src/main.py
```

## Architecture

The application uses a registry-based architecture where:

1. **Controls** define security policies and validation logic
2. **Generators** create artifacts from control settings
3. **UI Renderers** handle user interface for each control type
4. **Services** coordinate between components

## Documentation Structure

- [`architecture.md`](architecture.md) - System architecture overview
- [`system-overview.md`](system-overview.md) - Complete system functionality overview
- [`getting-started.md`](getting-started.md) - User guide and tutorial
- [`extension-guide.md`](extension-guide.md) - **Step-by-step instructions for adding new controls and generators**
- [`core/`](core/) - Core interfaces and base classes
- [`controls/`](controls/) - Security control implementations
- [`generators/`](generators/) - Artifact generation engines
- [`ui/`](ui/) - User interface components
- [`services/`](services/) - Business logic services
- [`examples/`](examples/) - Usage examples and extension patterns

## Security Notice

⚠️ **Always test configurations in a non-production environment first!**

Generated artifacts can significantly impact system behavior and security posture.
